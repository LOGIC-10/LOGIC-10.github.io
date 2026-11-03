function initializeLibrary(root: HTMLElement) {
  if (root.dataset.libraryReady) return;
  const cards = [...root.querySelectorAll<HTMLElement>('[data-paper]')];
  const search = root.querySelector<HTMLInputElement>('[data-research-search]')!;
  const filters = [...root.querySelectorAll<HTMLButtonElement>('[data-filter]')];
  const count = root.querySelector<HTMLElement>('[data-result-count]')!;
  const empty = root.querySelector<HTMLElement>('[data-no-results]')!;
  const pageSize = Number(root.dataset.pageSize) || 10;
  let page = 1;
  let area = 'all';
  let totalPages = 1;

  function updateResults() {
    const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const matching = cards.filter(card =>
      (area === 'all' || (card.dataset.topics || '').toLowerCase().includes(area)) &&
      words.every(word => (card.dataset.title || '').includes(word))
    );
    totalPages = Math.max(1, Math.ceil(matching.length / pageSize));
    page = Math.max(1, Math.min(page, totalPages));
    const offset = (page - 1) * pageSize;
    const visible = new Set(matching.slice(offset, offset + pageSize));
    cards.forEach(card => { card.hidden = !visible.has(card); });
    const start = matching.length ? offset + 1 : 0;
    const end = Math.min(offset + pageSize, matching.length);
    count.textContent = `Showing ${start}–${end} of ${matching.length} work${matching.length === 1 ? '' : 's'}`;
    empty.hidden = matching.length > 0;
    filters.forEach(button => {
      const selected = button.dataset.filter === area;
      button.classList.toggle('is-selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    root.querySelectorAll<HTMLElement>('.publication-pagination').forEach(nav => {
      nav.hidden = totalPages <= 1;
      nav.querySelector<HTMLButtonElement>('[data-page-prev]')!.disabled = page === 1;
      nav.querySelector<HTMLButtonElement>('[data-page-next]')!.disabled = page === totalPages;
      nav.querySelector<HTMLElement>('[data-page-summary]')!.textContent = `Page ${page} of ${totalPages}`;
      const numbers = nav.querySelector<HTMLElement>('[data-page-numbers]')!;
      const select = nav.querySelector<HTMLSelectElement>('[data-page-select]')!;
      numbers.replaceChildren();
      select.replaceChildren();
      for (let number = 1; number <= totalPages; number++) {
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.pageNumber = String(number);
        button.textContent = String(number);
        button.setAttribute('aria-label', `Go to page ${number}`);
        button.setAttribute('aria-controls', root.querySelector('[data-publication-list]')!.id);
        if (number === page) button.setAttribute('aria-current', 'page');
        numbers.append(button);
        const option = document.createElement('option');
        option.value = String(number);
        option.textContent = String(number);
        select.append(option);
      }
      select.value = String(page);
    });
    root.dataset.currentPage = String(page);
    root.dataset.matchingCount = String(matching.length);
  }

  function changePage(number: number) {
    if (number === page || number < 1 || number > totalPages) return;
    page = number;
    updateResults();
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    root.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    root.querySelector<HTMLButtonElement>(`[data-pagination-top] [data-page-number="${page}"]`)?.focus({ preventScroll: true });
  }

  root.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    const button = event.target.closest<HTMLButtonElement>('button');
    if (!button || !root.contains(button)) return;
    if (button.hasAttribute('data-page-prev')) changePage(page - 1);
    else if (button.hasAttribute('data-page-next')) changePage(page + 1);
    else if (button.dataset.pageNumber) changePage(Number(button.dataset.pageNumber));
    else if (button.dataset.filter) {
      area = button.dataset.filter;
      page = 1;
      updateResults();
    } else if (button.hasAttribute('data-reset-search')) {
      search.value = '';
      area = 'all';
      page = 1;
      updateResults();
      search.focus();
    }
  });
  root.querySelectorAll<HTMLSelectElement>('[data-page-select]').forEach(select => select.addEventListener('change', () => changePage(Number(select.value))));
  search.addEventListener('input', () => { page = 1; updateResults(); });
  root.querySelector<HTMLElement>('[data-research-controls]')!.hidden = false;
  updateResults();
  root.dataset.libraryReady = 'true';
}

export function initializePublicationLibraries() {
  document.querySelectorAll<HTMLElement>('[data-publication-library]').forEach(initializeLibrary);
}
