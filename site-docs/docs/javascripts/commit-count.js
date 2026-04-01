/**
 * Fetches total commit count from the GitHub API and displays it
 * in the #commit-count-badge element on the landing page.
 *
 * Uses the Link header pagination trick: request 1 commit per page,
 * read the last page number from the Link header — that IS the count.
 */

;(function () {
    const GITHUB_REPO = 'trobz/odoo-addons-path';

    function formatCount(n) {
        if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
        return String(n);
    }

    async function fetchCommitCount() {
        const badge = document.getElementById('commit-count-badge');
        const label = document.getElementById('commit-count-label');
        if (!badge || !label) return;

        try {
            const res = await fetch(
                `https://api.github.com/repos/${GITHUB_REPO}/commits?per_page=1`,
                { headers: { Accept: 'application/vnd.github+json' } }
            );
            if (!res.ok) return;

            const link = res.headers.get('Link') || '';
            const match = link.match(/[?&]page=(\d+)>;\s*rel="last"/);
            if (!match) return;

            const total = parseInt(match[1], 10);
            label.textContent = `${formatCount(total)} commits`;
            badge.style.display = '';
        } catch (_) {
            // Silently fail — badge stays hidden
        }
    }

    if (typeof document$ !== 'undefined') {
        document$.subscribe(fetchCommitCount);
    } else if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fetchCommitCount);
    } else {
        fetchCommitCount();
    }
})();
