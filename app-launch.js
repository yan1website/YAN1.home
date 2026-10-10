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
    if (relativePath === 'index.html' && !targetURL.search) return appRoot;
    if (relativePath === 'index.html') {
      const routeParams = new URLSearchParams(targetURL.search);
      const requestedPage = routeParams.get('page')
        || [...routeParams.keys()].find(key => key.endsWith('.html'));
      return requestedPage && requestedPage !== 'index.html' ? targetURL : null;
    }
    if (!relativePath.endsWith('.html')) return null;
    if (relativePath.split('/').some(segment => !segment || segment === '.' || segment === '..')) return null;

    const viewerURL = new URL('index.html', appRoot);
    viewerURL.search = `?${encodeURIComponent(relativePath)}`;
    targetURL.searchParams.forEach((value, key) => viewerURL.searchParams.append(key, value));
    viewerURL.hash = targetURL.hash;
    return viewerURL;
  }

  document.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0
      || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey
      || link.hasAttribute('download') || link.id === 'website-list-link') return;

    const targetURL = new URL(link.href, window.location.href);
    const viewerURL = viewerURLFor(targetURL);
    if (!viewerURL) return;

    event.preventDefault();
    try {
      window.top.location.assign(viewerURL.href);
    } catch (error) {
      console.error('Could not open the linked page in the YAN1 viewer.', error);
      window.location.assign(viewerURL.href);
    }
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
