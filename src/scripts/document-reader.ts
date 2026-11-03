import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist';
import { EventBus, PDFFindController, PDFLinkService, PDFViewer } from 'pdfjs-dist/web/pdf_viewer.mjs';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';

GlobalWorkerOptions.workerSrc = workerUrl;

function initializeReader(root: HTMLElement) {
  if (root.dataset.readerInitialized) return;
  root.dataset.readerInitialized = 'true';
  const container = root.querySelector<HTMLDivElement>('[data-document-container]')!;
  const pages = root.querySelector<HTMLDivElement>('[data-document-viewer]')!;
  const status = root.querySelector<HTMLElement>('[data-document-status]')!;
  const pageInput = root.querySelector<HTMLInputElement>('[data-document-page]')!;
  const previous = root.querySelector<HTMLButtonElement>('[data-document-prev]')!;
  const next = root.querySelector<HTMLButtonElement>('[data-document-next]')!;
  const zoom = root.querySelector<HTMLSelectElement>('[data-document-zoom]')!;
  const search = root.querySelector<HTMLInputElement>('[data-document-search]')!;
  const find = root.querySelector<HTMLButtonElement>('[data-document-find]')!;
  const expand = root.querySelector<HTMLButtonElement>('[data-document-expand]')!;
  const retry = root.querySelector<HTMLButtonElement>('[data-document-retry]')!;
  const matches = root.querySelector<HTMLOutputElement>('[data-document-matches]')!;
  let viewer: PDFViewer | undefined;
  let eventBus: EventBus | undefined;
  let loading = false;
  let loaded = false;

  function updatePageControls() {
    if (!viewer) return;
    pageInput.value = String(viewer.currentPageNumber);
    previous.disabled = viewer.currentPageNumber <= 1;
    next.disabled = viewer.currentPageNumber >= viewer.pagesCount;
  }

  function runSearch(again = false) {
    if (!eventBus || !loaded) return;
    eventBus.dispatch('find', {
      source: search,
      type: again ? 'again' : '',
      query: search.value,
      phraseSearch: true,
      caseSensitive: false,
      entireWord: false,
      highlightAll: true,
      findPrevious: false,
    });
    if (!search.value) matches.textContent = '';
  }

  async function load() {
    if (loading || loaded) return;
    loading = true;
    root.dataset.readerState = 'loading';
    status.hidden = false;
    status.textContent = 'Loading document…';
    retry.hidden = true;
    try {
      eventBus = new EventBus();
      const linkService = new PDFLinkService({ eventBus, externalLinkTarget: 2 });
      const findController = new PDFFindController({ eventBus, linkService });
      viewer = new PDFViewer({
        container,
        viewer: pages,
        eventBus,
        linkService,
        findController,
        annotationMode: 0,
        textLayerMode: 1,
        imagesRightClickMinSize: -1,
        enablePermissions: false,
      });
      linkService.setViewer(viewer);
      eventBus.on('pagesinit', () => {
        viewer!.currentScaleValue = zoom.value;
        root.dataset.readerState = 'ready';
        status.hidden = true;
        [pageInput, zoom, search, find].forEach(control => control.disabled = false);
        updatePageControls();
      });
      eventBus.on('pagechanging', updatePageControls);
      eventBus.on('pagerendered', () => { root.dataset.renderedPages = String(pages.querySelectorAll('canvas').length); });
      eventBus.on('updatefindmatchescount', (event: { matchesCount?: { current: number; total: number } }) => {
        if (event.matchesCount && search.value) matches.textContent = `${event.matchesCount.current} / ${event.matchesCount.total}`;
      });
      const document = await getDocument({
        url: root.dataset.documentUrl!,
        cMapUrl: '/pdfjs/cmaps/',
        cMapPacked: true,
        standardFontDataUrl: '/pdfjs/standard_fonts/',
        wasmUrl: '/pdfjs/wasm/',
        iccUrl: '/pdfjs/iccs/',
        isEvalSupported: false,
        enableXfa: false,
      }).promise;
      viewer.setDocument(document);
      linkService.setDocument(document, null);
      pageInput.max = String(document.numPages);
      root.querySelector('.document-total')!.textContent = `/ ${document.numPages}`;
      loaded = true;
      root.dataset.actualPages = String(document.numPages);
    } catch (error) {
      console.error('Document reader could not load', root.dataset.documentUrl, error);
      root.dataset.readerState = 'error';
      status.textContent = 'This document could not be displayed. Please try again.';
      retry.hidden = false;
    } finally {
      loading = false;
    }
  }

  previous.addEventListener('click', () => { if (viewer && loaded) viewer.currentPageNumber = Math.max(1, viewer.currentPageNumber - 1); });
  next.addEventListener('click', () => { if (viewer && loaded) viewer.currentPageNumber = Math.min(viewer.pagesCount, viewer.currentPageNumber + 1); });
  function goToEnteredPage() {
    if (!viewer || !loaded) return;
    viewer.currentPageNumber = Math.max(1, Math.min(viewer.pagesCount, Math.trunc(Number(pageInput.value)) || 1));
    updatePageControls();
  }
  pageInput.addEventListener('change', goToEnteredPage);
  pageInput.addEventListener('blur', goToEnteredPage);
  pageInput.addEventListener('keydown', event => {
    if (event.key === 'Enter') { event.preventDefault(); goToEnteredPage(); }
  });
  zoom.addEventListener('change', () => { if (viewer && loaded) viewer.currentScaleValue = zoom.value; });
  find.addEventListener('click', () => runSearch(true));
  search.addEventListener('keydown', event => { if (event.key === 'Enter') { event.preventDefault(); runSearch(true); } });
  let searchTimer: ReturnType<typeof setTimeout>;
  search.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(() => runSearch(), 200); });

  function setExpanded(value: boolean) {
    root.classList.toggle('is-expanded', value);
    expand.setAttribute('aria-pressed', String(value));
    expand.setAttribute('aria-label', value ? 'Close expanded reader' : 'Expand reader');
    expand.textContent = value ? 'Close ×' : 'Expand ↗';
    if (viewer && loaded) requestAnimationFrame(() => { viewer!.currentScaleValue = zoom.value; viewer!.update(); });
  }
  expand.addEventListener('click', () => setExpanded(!root.classList.contains('is-expanded')));
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && root.classList.contains('is-expanded')) { setExpanded(false); expand.focus(); } });
  new ResizeObserver(() => {
    if (viewer && loaded && zoom.value.startsWith('page-')) viewer.currentScaleValue = zoom.value;
  }).observe(container);
  retry.addEventListener('click', () => { viewer?.setDocument(null); pages.replaceChildren(); load(); });
  const observer = new IntersectionObserver(entries => {
    if (entries.some(entry => entry.isIntersecting)) { observer.disconnect(); load(); }
  }, { rootMargin: '550px 0px' });
  observer.observe(root);
}

export function initializeDocumentReaders() {
  document.querySelectorAll<HTMLElement>('[data-document-reader]').forEach(initializeReader);
}
