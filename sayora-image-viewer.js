(() => {
	const imageSelector = 'img.field-image, img.cell-image';
	const style = document.createElement('style');
	style.textContent = `
		${imageSelector} { cursor: zoom-in; }
		#sayoraImageViewer {
			position: fixed;
			inset: 0;
			width: 100vw;
			max-width: none;
			max-height: none;
			height: 100dvh;
			margin: 0;
			padding: 56px 20px 20px;
			border: 0;
			color: #fff;
			background: #08090df2;
		}
		#sayoraImageViewer::backdrop { background: #08090df2; }
		#sayoraImageViewer img {
			display: block;
			width: 100%;
			height: 100%;
			object-fit: contain;
		}
		#sayoraImageViewerClose {
			position: fixed;
			top: max(12px, env(safe-area-inset-top));
			right: max(12px, env(safe-area-inset-right));
			min-width: 44px;
			min-height: 44px;
			border: 1px solid #777;
			border-radius: 6px;
			color: #fff;
			background: #25262b;
			font: inherit;
			font-size: 28px;
			line-height: 1;
			cursor: pointer;
		}
		#sayoraImageViewerClose:hover { background: #3a3b42; }
		@media (max-width: 520px) { #sayoraImageViewer { padding: 64px 10px 10px; } }
	`;
	document.head.appendChild(style);

	const viewer = document.createElement('dialog');
	viewer.id = 'sayoraImageViewer';
	viewer.setAttribute('aria-label', 'Fullscreen image viewer');
	const closeButton = document.createElement('button');
	closeButton.id = 'sayoraImageViewerClose';
	closeButton.type = 'button';
	closeButton.setAttribute('aria-label', 'Close image');
	closeButton.title = 'Close image';
	closeButton.textContent = '×';
	const viewerImage = document.createElement('img');
	viewerImage.alt = '';
	viewer.append(closeButton, viewerImage);
	document.body.appendChild(viewer);

	function prepareImage(image) {
		image.tabIndex = 0;
		image.setAttribute('role', 'button');
		image.setAttribute('aria-label', image.alt ? `View full-screen image: ${image.alt}` : 'View full-screen image');
	}

	function prepareImages(root) {
		if (root.matches?.(imageSelector)) prepareImage(root);
		root.querySelectorAll?.(imageSelector).forEach(prepareImage);
	}

	function openViewer(image) {
		viewerImage.src = image.currentSrc || image.src;
		viewerImage.alt = image.alt;
		viewer.showModal();
		closeButton.focus();
	}

	prepareImages(document);
	new MutationObserver((records) => {
		for (const record of records) {
			for (const node of record.addedNodes) {
				if (node.nodeType === Node.ELEMENT_NODE) prepareImages(node);
			}
		}
	}).observe(document.body, { childList: true, subtree: true });

	document.addEventListener('click', (event) => {
		if (!(event.target instanceof Element)) return;
		const image = event.target.closest(imageSelector);
		if (image) openViewer(image);
	});

	document.addEventListener('keydown', (event) => {
		if (!(event.target instanceof Element) || !event.target.matches(imageSelector)) return;
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			openViewer(event.target);
		}
	});

	closeButton.addEventListener('click', () => viewer.close());
	viewer.addEventListener('click', (event) => {
		if (event.target === viewer) viewer.close();
	});
	viewer.addEventListener('close', () => {
		viewerImage.removeAttribute('src');
	});
})();