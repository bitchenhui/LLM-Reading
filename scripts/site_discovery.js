// Shared browser/Node retrieval logic. Matches recorded text, not semantic answers.
function containsTerm(text, term) {
  text = text.toLowerCase();
  term = term.toLowerCase();
  let start = text.indexOf(term);
  while (start !== -1) {
    const leftOK = !/^[a-z0-9]/.test(term) || !/[a-z0-9]/.test(text[start - 1] || '');
    const rightOK = !/[a-z0-9]$/.test(term) || !/[a-z0-9]/.test(text[start + term.length] || '');
    if (leftOK && rightOK) return true;
    start = text.indexOf(term, start + 1);
  }
  return false;
}
function claimText(claim) {
  return [claim.statement, ...(claim.metrics || []).map(m => [m.name, m.ref, m.value, m.scope].filter(Boolean).join(' '))].join(' ');
}
function searchEvidence(query, items, topics) {
  const normalized = query.toLowerCase().trim();
  const matchedTopics = topics.filter(t => t.terms.some(term => term.length >= 2 && containsTerm(normalized, term)));
  // Do not require a nested alias twice (e.g. AV1 inside SVT-AV1).
  const selectedTopics = matchedTopics.filter(t => !matchedTopics.some(other => other !== t &&
    other.terms.some(long => containsTerm(normalized, long) && t.terms.some(short => long.length > short.length && containsTerm(long, short)))));
  const focusGroups = [
    ['码率', '压缩', 'bitrate', 'bd-rate'], ['解码', 'decode', 'decoding'],
    ['编码速度', '编码时间', '加速', 'encoding time'], ['画质', '质量', 'psnr', 'vmaf'],
    ['内存', 'memory'], ['功耗', '能耗', 'energy']
  ];
  const focus = focusGroups.filter(g => g.some(term => containsTerm(normalized, term))).flat();
  let remainder = normalized;
  for (const topic of selectedTopics) for (const term of [...topic.terms].sort((a,b) => b.length - a.length)) {
    remainder = remainder.split(term.toLowerCase()).join(' ');
  }
  remainder = remainder.replace(/怎么|如何|有哪些|有什么|什么|是否|可以|能不能|有没有|的|了|吗|呢|请问|相关|研究|证据|依据|优化|方向|介绍|了解/g, ' ');
  const terms = remainder.split(/[\s，。？！、,?!;；]+/).filter(Boolean);
  const focusScore = text => focus.reduce((n, t) => n + Number(containsTerm(text, t)), 0);
  const matches = [];
  for (const item of items) {
    const title = [item.title, item.orig_title, item.id].join(' ');
    const evidence = (item.claims || []).map(claimText).join(' ');
    const protocol = Object.values(item.protocol || {}).join(' ');
    const all = [title, item.one_liner, item.entities.join(' '), evidence, protocol].join(' ');
    const topicMatch = selectedTopics.every(t => item.entities.includes(t.id) || t.terms.some(term => containsTerm(all, term)));
    const termScores = terms.map(t => containsTerm(title, t) ? 8 : containsTerm(evidence + ' ' + protocol, t) ? 4 : containsTerm(all, t) ? 1 : 0);
    if (selectedTopics.length ? !topicMatch : !terms.length || !termScores.every(Boolean)) continue;
    const claims = (item.claims || []).map((claim, index) => ({claim, index,
      score: focusScore(claimText(claim)) * 6 + terms.filter(t => containsTerm(claimText(claim), t)).length * 3
        + Number(Boolean(claim.evidence_url))
    })).sort((a,b) => b.score - a.score || a.index - b.index).map(c => c.claim);
    const score = termScores.reduce((a,b) => a+b,0) + focusScore(evidence) * 6
      + (item.type === 'paper' ? 3 : 0) + (claims.some(c => c.evidence_url) ? 2 : 0);
    matches.push({item, claims, score});
  }
  matches.sort((a,b) => b.score - a.score || b.item.published.localeCompare(a.item.published));
  return {matches, topics: selectedTopics, terms};
}

function sourceLink(url, label) {
  return /^https?:\/\//i.test(url || '') ? `<a href="${esc(url)}">${esc(label)} ↗</a>` : '';
}
function evidenceHTML(item, claim) {
  const label = {reported:'来源报告', verified:'已复测', inferred:'推断'}[claim.confidence] || '状态待补';
  const url = `${item.detail}/${encodeURIComponent(claim.id)}`;
  const metrics = (claim.metrics || []).map(m => {
    const value = String(m.value);
    const unit = m.unit && !value.endsWith(m.unit) ? m.unit : '';
    return `<li><b>${esc(m.name || m.ref || '指标')} ${esc(value + unit)}</b><span>${esc(m.scope || '实验条件待补')}</span></li>`;
  }).join('');
  const source = claim.evidence_url ? sourceLink(claim.evidence_url, claim.evidence || '原文对应位置')
    : sourceLink(item.url, '原文（精确定位待补）');
  return `<section class="evidence"><span class="confidence">${label}</span><p>${esc(claim.statement)}</p>
    ${metrics ? `<details class="conditions"><summary>查看指标与适用条件</summary><ul>${metrics}</ul></details>` : ''}
    <div class="evidence-links"><a href="${esc(url)}">查看完整论断</a>${source}</div></section>`;
}
function resultHTML(hit) {
  const {item, claims} = hit;
  const first = claims.slice(0,2).map(c => evidenceHTML(item,c)).join('');
  const more = claims.length > 2 ? `<details class="more-evidence"><summary>其余 ${claims.length - 2} 条论断</summary>${claims.slice(2).map(c => evidenceHTML(item,c)).join('')}</details>` : '';
  return `<article class="result-card"><div class="meta">${esc(DN[item.domain] || item.domain)} · ${esc(item.published)} · ${item.type === 'repo_release' ? '版本动态' : '研究资料'}</div>
    <h3><a href="${esc(item.detail)}">${esc(item.title)}</a></h3><p class="result-summary">${esc(item.one_liner)}</p>
    ${first || '<p class="note">暂无结构化论断，请查阅原文。</p>'}${more}
    <div class="evidence-links">${item.deep ? sourceLink(item.deep, '精读笔记') : ''}<a href="${esc(item.detail)}">条目详情 →</a></div></article>`;
}
function renderDiscovery(query) {
  const items = Object.values(DATA.items_by_domain).flat();
  document.getElementById('coverage').textContent = `已收录 ${DATA.stats.total} 条资料 · 更新于 ${DATA.generated} · 收录范围有限，未找到证据不代表不存在相关研究。`;
  const popular = ['impl:VVenC', 'codec:VVC', 'codec:AV1', 'codec:Opus', 'concept:NeuralAudioCodec', 'concept:WebRTC'];
  document.getElementById('topicLinks').innerHTML = popular.map(id => DATA.topics.find(t => t.id === id)).filter(Boolean)
    .map(t => `<a href="?q=${encodeURIComponent(t.name)}">${esc(t.name)} →</a>`).join('');
  if (!query) return;
  document.title = query + ' · 音视频知识库';
  document.getElementById('searchQuery').value = query;
  document.getElementById('discoveryHome').hidden = true;
  const results = document.getElementById('searchResults');
  results.hidden = false;
  const found = searchEvidence(query, items, DATA.topics);
  const {matches, topics} = found;
  const dossier = topics.length === 1 ? DATA.dossiers.find(d => d.id === topics[0].id.replace(':','_')) : null;
  const overview = topics.length === 1 ? `<aside class="topic-overview"><span class="eyebrow">技术主题</span><h2>${esc(topics[0].name)}</h2>
    <p>${esc(topics[0].description || '从以下已收录的结论开始，核对各项研究的适用范围。')}</p>
    ${dossier ? `<details><summary>阅读技术背景与发展脉络</summary><p class="note">以下为合成综述；具体结论请核对下方条目证据。</p><div class="body">${md2html(dossier.md)}</div></details>` : ''}</aside>` : '';
  results.innerHTML = `<h1 class="results-title">与“${esc(query)}”相关的证据</h1>
    <p class="note">${topics.length ? '识别技术：' + topics.map(t => esc(t.name)).join('、') + '。围绕该技术召回资料，并按问题中的关键词排序。' : '按关键词匹配标题、摘要、论断和实验条件。'}相关资料不一定直接支持问题中的假设。</p>
    ${overview}<div class="result-toolbar"><h2 id="resultCount"></h2><label><input id="preciseOnly" type="checkbox"> 仅看有原文定位的论断</label></div>
    <div id="hits"></div><button class="tab" id="moreResults">更多结果</button>`;
  let active = matches, shown = 0;
  const hits = document.getElementById('hits');
  const more = document.getElementById('moreResults');
  function nextPage() {
    const page = active.slice(shown, shown + 8);
    hits.insertAdjacentHTML('beforeend', page.map(resultHTML).join(''));
    shown += page.length;
    more.hidden = shown >= active.length;
  }
  function refresh() {
    const precise = document.getElementById('preciseOnly').checked;
    active = precise ? matches.map(hit => ({...hit, claims: hit.claims.filter(c => /^https?:\/\//i.test(c.evidence_url || ''))})).filter(hit => hit.claims.length) : matches;
    shown = 0;
    document.getElementById('resultCount').textContent = `${active.length} 条资料 · ${active.reduce((n,h) => n+h.claims.length,0)} 条论断`;
    hits.innerHTML = active.length ? '' : '<div class="empty"><h2>没有找到符合条件的证据</h2><p>试试更具体的技术名（如 VVenC）、数据集（如 Inter-4K），或取消原文定位筛选。</p><a href="?view=kb">按技术主题浏览 →</a></div>';
    nextPage();
  }
  more.onclick = nextPage;
  document.getElementById('preciseOnly').onchange = refresh;
  refresh();
}
if (typeof module !== 'undefined') module.exports = {containsTerm, searchEvidence};
