(() => {
  const launcher = [...document.scripts].find(script => /(?:^|\/)app-launch\.js(?:[?#]|$)/.test(script.src));
  const appRoot = launcher ? new URL('index.html', launcher.src) : new URL('index.html', window.location.href);
  const appRootPath = appRoot.pathname.slice(0, appRoot.pathname.lastIndexOf('/') + 1);

  function viewerURLFor(targetURL) {
    if (targetURL.origin !== appRoot.origin || !targetURL.pathname.startsWith(appRootPath)) return null;
    const relativePath = targetURL.pathname.slice(appRootPath.length).split('/').map(segment => {
      try {
        return decodeURIComponent(segment);
      } catch (_) {
        return segment;
      }
    }).join('/');
    let pagePath = relativePath;
    let pageParams = new URLSearchParams(targetURL.search);
    if (relativePath === 'index.html') {
      pagePath = pageParams.get('page')
        || [...pageParams.keys()].find(key => key.endsWith('.html'));
      if (!pagePath || pagePath === 'index.html') return null;
      const routeKey = pageParams.has('page')
        ? 'page'
        : [...pageParams.keys()].find(key => key.endsWith('.html'));
      pageParams.delete(routeKey);
    }
    if (!pagePath.endsWith('.html')
      || pagePath.split('/').some(segment => !segment || segment === '.' || segment === '..')) return null;

    const viewerURL = new URL('index.html', appRoot);
    const remainingQuery = pageParams.toString();
    viewerURL.search = `?${encodeURIComponent(pagePath)}${remainingQuery ? `&${remainingQuery}` : ''}`;
    viewerURL.hash = targetURL.hash;
    return {
      filename: pagePath,
      search: pageParams.toString(),
      hash: targetURL.hash,
      url: viewerURL.href
    };
  }

  document.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0
      || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey
      || link.hasAttribute('download') || link.id === 'website-list-link') return;

    const targetURL = new URL(link.href, window.location.href);
    const destination = viewerURLFor(targetURL);
    if (!destination) return;

    event.preventDefault();
    window.top.location.assign(destination.url);
  }, true);

  if (window.top !== window.self) return;
  if (window.AndroidPython && typeof window.AndroidPython.executePython === 'function') return;

  const pageURL = new URL(window.location.href);
  if (pageURL.pathname.endsWith('/download_app.html')) return;
  if (pageURL.protocol !== 'http:' && pageURL.protocol !== 'https:') return;
  if (pageURL.hostname === '127.0.0.1' || pageURL.hostname === 'localhost') return;

  const pageKey = `yan1_launched:${pageURL.pathname}${pageURL.search}`;
  try {
    if (sessionStorage.getItem(pageKey) === 'true') return;
    sessionStorage.setItem(pageKey, 'true');
  } catch (_) {}

  const fallbackURL = new URL('download_app.html', appRoot).href;
  const intentURL = `intent://${pageURL.host}${pageURL.pathname}${pageURL.search}#Intent;scheme=${pageURL.protocol.slice(0, -1)};package=com.example1.yan1appgen1;S.browser_fallback_url=${encodeURIComponent(fallbackURL)};end;`;
  setTimeout(() => window.location.replace(intentURL), 1200);
})();
