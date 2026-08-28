(function () {
    const competitions = [
        { id: "oma", label: "OMA", group: "national", legacyHash: "oma" },
        { id: "nandu", label: "Ñandú", group: "national", legacyHash: "omn" },
        { id: "provinciales", label: "Provinciales", group: "national", legacyHash: "pro" },
        { id: "pretorneos", label: "Pretorneos", group: "national", legacyHash: "ptic" },
        { id: "imo", label: "IMO", group: "international", legacyHash: "imo" },
        { id: "iberoamericana", label: "Iberoamericana", group: "international", legacyHash: "ibero" },
        { id: "cono-sur", label: "Cono Sur", group: "international", legacyHash: "cono" },
        { id: "rioplatense", label: "Rioplatense", group: "international", legacyHash: "omr" },
        { id: "cuenca-pacifico", label: "Cuenca del Pacifico", group: "international", legacyHash: "cuenca" },
        { id: "mayo", label: "Mayo", group: "international", legacyHash: "may" },
        { id: "torneo-ciudades", label: "Torneo de las Ciudades", group: "international", legacyHash: "tic" },
        { id: "irani-geometria", label: "Iraní de Geometria", group: "international", legacyHash: "igo" }
    ];

    const competitionByHash = {};
    competitions.forEach(function (competition) {
        competitionByHash[competition.id] = competition.id;
        competitionByHash[competition.legacyHash] = competition.id;
    });

    let archiveItems = [];
    let currentCompetition = "all";
    let currentYear = "all";
    let currentPage = 1;
    const pageSize = 8;

    function createFilterButton(competition) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "filter-button";
        button.dataset.competition = competition.id;
        button.textContent = competition.label;
        button.addEventListener("click", function () {
            currentCompetition = competition.id;
            currentPage = 1;
            if (competition.id === "all") {
                history.replaceState(null, "", window.location.pathname + window.location.search);
            } else {
                window.location.hash = competition.legacyHash;
            }
            renderArchive();
        });
        return button;
    }

    function renderFilters() {
        const nationalFilters = document.getElementById("national-filters");
        const internationalFilters = document.getElementById("international-filters");
        nationalFilters.innerHTML = "";
        internationalFilters.innerHTML = "";

        nationalFilters.appendChild(createFilterButton({ id: "all", label: "Todos", legacyHash: "" }));
        competitions.forEach(function (competition) {
            const button = createFilterButton(competition);
            if (competition.group === "national") {
                nationalFilters.appendChild(button);
            } else {
                internationalFilters.appendChild(button);
            }
        });
    }

    function renderYearOptions() {
        const yearFilter = document.getElementById("year-filter");
        const years = Array.from(new Set(archiveItems.map(function (item) {
            return Number(item.year);
        }))).filter(Boolean).sort(function (a, b) {
            return b - a;
        });

        yearFilter.innerHTML = "";
        const allOption = document.createElement("option");
        allOption.value = "all";
        allOption.textContent = "Todos";
        yearFilter.appendChild(allOption);

        years.forEach(function (year) {
            const option = document.createElement("option");
            option.value = String(year);
            option.textContent = String(year);
            yearFilter.appendChild(option);
        });

        yearFilter.value = currentYear;
        yearFilter.addEventListener("change", function () {
            currentYear = yearFilter.value;
            currentPage = 1;
            renderArchive();
        });
    }

    function filteredItems() {
        return archiveItems
            .filter(function (item) {
                if (item.visible === false) {
                    return false;
                }
                if (currentCompetition !== "all" && item.competition !== currentCompetition) {
                    return false;
                }
                if (currentYear !== "all" && String(item.year) !== currentYear) {
                    return false;
                }
                return Array.isArray(item.files) && item.files.length > 0;
            })
            .sort(function (left, right) {
                if (Number(right.year) !== Number(left.year)) {
                    return Number(right.year) - Number(left.year);
                }
                return competitions.findIndex(function (competition) {
                    return competition.id === left.competition;
                }) - competitions.findIndex(function (competition) {
                    return competition.id === right.competition;
                });
            });
    }

    function createFileLink(file) {
        const link = document.createElement("a");
        link.href = file.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = file.label + " ↗";
        return link;
    }

    function createEntry(item) {
        const article = document.createElement("article");
        article.className = "archive-entry";

        const heading = document.createElement("h2");
        heading.textContent = item.title + " (" + item.year + ")";
        article.appendChild(heading);

        const links = document.createElement("div");
        links.className = "archive-links";
        item.files.forEach(function (file) {
            links.appendChild(createFileLink(file));
        });
        article.appendChild(links);

        return article;
    }

    function renderList(items) {
        const archiveList = document.getElementById("archive-list");
        const archiveCount = document.getElementById("archive-count");
        archiveList.innerHTML = "";

        if (!items.length) {
            archiveCount.textContent = "";
            const empty = document.createElement("div");
            empty.className = "archive-empty";
            empty.textContent = "No hay enunciados cargados para esos filtros.";
            archiveList.appendChild(empty);
            return;
        }

        const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
        if (currentPage > totalPages) {
            currentPage = totalPages;
        }
        const pageItems = items.slice((currentPage - 1) * pageSize, currentPage * pageSize);
        archiveCount.textContent = items.length + " registros";
        pageItems.forEach(function (item) {
            archiveList.appendChild(createEntry(item));
        });
    }

    function paginationButton(label, disabled, active, onClick) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "page-button";
        button.textContent = label;
        button.disabled = disabled;
        if (active) {
            button.classList.add("active");
            button.setAttribute("aria-current", "page");
        }
        button.addEventListener("click", onClick);
        return button;
    }

    function renderPagination(items) {
        const pagination = document.getElementById("archive-pagination");
        const totalPages = Math.ceil(items.length / pageSize);
        pagination.innerHTML = "";
        if (totalPages <= 1) {
            return;
        }

        pagination.appendChild(paginationButton("‹", currentPage === 1, false, function () {
            currentPage -= 1;
            renderArchive();
        }));

        for (let page = 1; page <= totalPages; page += 1) {
            if (page > 3 && page < totalPages - 1 && Math.abs(page - currentPage) > 1) {
                if (!pagination.querySelector("[data-ellipsis]")) {
                    const span = document.createElement("span");
                    span.dataset.ellipsis = "true";
                    span.textContent = "...";
                    pagination.appendChild(span);
                }
                continue;
            }
            pagination.appendChild(paginationButton(String(page), false, page === currentPage, function () {
                currentPage = page;
                renderArchive();
            }));
        }

        pagination.appendChild(paginationButton("›", currentPage === totalPages, false, function () {
            currentPage += 1;
            renderArchive();
        }));
    }

    function markActiveFilters() {
        document.querySelectorAll(".filter-button").forEach(function (button) {
            button.classList.toggle("active", button.dataset.competition === currentCompetition);
        });
    }

    function renderArchive() {
        const items = filteredItems();
        markActiveFilters();
        renderList(items);
        renderPagination(items);
    }

    function setInitialCompetitionFromHash() {
        const hash = window.location.hash.replace("#", "").trim();
        if (hash && competitionByHash[hash]) {
            currentCompetition = competitionByHash[hash];
        }
    }

    function loadArchive() {
        fetch("/contents/enunciados/index.json", { cache: "no-store" })
            .then(function (response) {
                if (!response.ok) {
                    return { items: [] };
                }
                return response.json();
            })
            .then(function (archive) {
                archiveItems = Array.isArray(archive.items) ? archive.items : [];
                setInitialCompetitionFromHash();
                renderFilters();
                renderYearOptions();
                renderArchive();
            })
            .catch(function () {
                archiveItems = [];
                renderFilters();
                renderYearOptions();
                renderArchive();
            });
    }

    window.addEventListener("hashchange", function () {
        const hash = window.location.hash.replace("#", "").trim();
        currentCompetition = competitionByHash[hash] || "all";
        currentPage = 1;
        renderArchive();
    });

    document.addEventListener("DOMContentLoaded", loadArchive);
})();
