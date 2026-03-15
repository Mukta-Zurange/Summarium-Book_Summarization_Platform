let token = localStorage.getItem("token") || "";

function showToast(message, type="primary") {
    const toastEl = document.getElementById("app-toast");
    const toastBody = document.getElementById("toast-message");
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    toastBody.innerText = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

function showLogin() {
    document.getElementById("login-form").style.display = "block";
    document.getElementById("register-form").style.display = "none";
    document.getElementById("forgot-form").style.display = "none";
    document.getElementById("login-tab").classList.add("active");
    document.getElementById("register-tab").classList.remove("active");
}

function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
    document.getElementById("forgot-form").style.display = "none";
    document.getElementById("register-tab").classList.add("active");
    document.getElementById("login-tab").classList.remove("active");
}

function switchInputType(type) {
    document.getElementById("file-upload-fields").style.display = type === "file" ? "block" : "none";
    document.getElementById("text-upload-fields").style.display = type === "text" ? "block" : "none";
    document.getElementById("upload-result").style.display = "none";
    document.getElementById("goto-summary-btn").style.display = "none";
}

async function register() {
    const question = document.getElementById("reg-security-question").value;
    const answer = document.getElementById("reg-security-answer").value.trim();

    if (!question || !answer) {
        showToast("Please select a security question and provide an answer", "danger");
        return;
    }

    const response = await fetch("/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("reg-name").value,
            email: document.getElementById("reg-email").value,
            password: document.getElementById("reg-password").value,
            security_question: question,
            security_answer: answer
        })
    });
    const data = await response.json();
    if (response.ok) {
        showToast("Registration successful!", "success");
        showLogin();
    } else {
        showToast(data.detail || "Registration failed", "danger");
    }
}

async function login() {
    const formData = new FormData();
    formData.append("username", document.getElementById("login-email").value);
    formData.append("password", document.getElementById("login-password").value);

    const selectedRole = getToggleValue("role-toggle");

    const response = await fetch("/login", { method: "POST", body: formData });
    const data = await response.json();

    if (response.ok) {
        if (data.role !== selectedRole) {
            showToast(
                selectedRole === "admin"
                    ? "This account does not have admin access."
                    : "Please use the Admin login for this account.",
                "danger"
            );
            return;
        }

        token = data.access_token;
        localStorage.setItem("token", token);
        localStorage.setItem("userRole", data.role);

        if (data.role === "admin") {
            window.location.href = "/admin";
        } else {
            document.getElementById("auth-section").style.display = "none";
            document.getElementById("dashboard").style.display = "block";
            showUpload();
            showToast("Login successful!", "success");
            await loadProfile();
        }
    } else {
        showToast(data.detail || "Login failed", "danger");
    }
}

function showForgotPassword() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("forgot-form").style.display = "block";
    document.getElementById("forgot-step-1").style.display = "block";
    document.getElementById("forgot-step-2").style.display = "none";
}

function showLoginFromForgot() {
    document.getElementById("forgot-form").style.display = "none";
    document.getElementById("login-form").style.display = "block";
}

async function fetchSecurityQuestion() {
    const email = document.getElementById("forgot-email").value.trim();
    if (!email) {
        showToast("Please enter your email", "danger");
        return;
    }

    const formData = new FormData();
    formData.append("email", email);

    const res = await fetch("/get-security-question", { method: "POST", body: formData });
    const data = await res.json();

    if (res.ok) {
        document.getElementById("security-question-text").innerText = data.question;
        document.getElementById("forgot-step-1").style.display = "none";
        document.getElementById("forgot-step-2").style.display = "block";
    } else {
        showToast(data.detail || "Email not found", "danger");
    }
}

async function resetPassword() {
    const email = document.getElementById("forgot-email").value.trim();
    const answer = document.getElementById("forgot-answer").value.trim();
    const newPassword = document.getElementById("forgot-new-password").value;
    const confirmPassword = document.getElementById("forgot-confirm-password").value;

    if (!answer) {
        showToast("Please enter your answer", "danger");
        return;
    }

    if (!newPassword || !confirmPassword) {
        showToast("Please fill in both password fields", "danger");
        return;
    }

    if (newPassword !== confirmPassword) {
        showToast("Passwords do not match", "danger");
        return;
    }

    const formData = new FormData();
    formData.append("email", email);
    formData.append("answer", answer);
    formData.append("new_password", newPassword);

    const res = await fetch("/reset-password", { method: "POST", body: formData });
    const data = await res.json();

    if (res.ok) {
        showToast("Password reset successfully! Please login.", "success");
        document.getElementById("forgot-form").style.display = "none";
        document.getElementById("login-form").style.display = "block";
    } else {
        showToast(data.detail || "Reset failed", "danger");
    }
}

function showUpload() {
    document.getElementById("upload-section").style.display = "block";
    document.getElementById("summary-section").style.display = "none";
    document.getElementById("books-section").style.display = "none";
    document.getElementById("mindmap-section").style.display = "none";
    document.getElementById("quiz-section").style.display = "none";
    document.getElementById("nav-upload").classList.add("active");
    document.getElementById("nav-summary").classList.remove("active");
    document.getElementById("nav-books").classList.remove("active");
    document.getElementById("nav-mindmap").classList.remove("active");
    document.getElementById("nav-quiz").classList.remove("active");
}

function showSummary() {
    document.getElementById("upload-section").style.display = "none";
    document.getElementById("summary-section").style.display = "block";
    document.getElementById("books-section").style.display = "none";
    document.getElementById("mindmap-section").style.display = "none";
    document.getElementById("quiz-section").style.display = "none";
    document.getElementById("nav-summary").classList.add("active");
    document.getElementById("nav-upload").classList.remove("active");
    document.getElementById("nav-books").classList.remove("active");
    document.getElementById("nav-mindmap").classList.remove("active");
    document.getElementById("nav-quiz").classList.remove("active");
}

function showBooks() {
    document.getElementById("upload-section").style.display = "none";
    document.getElementById("summary-section").style.display = "none";
    document.getElementById("books-section").style.display = "block";
    document.getElementById("mindmap-section").style.display = "none";
    document.getElementById("quiz-section").style.display = "none";
    document.getElementById("nav-books").classList.add("active");
    document.getElementById("nav-upload").classList.remove("active");
    document.getElementById("nav-summary").classList.remove("active");
    document.getElementById("nav-mindmap").classList.remove("active");
    document.getElementById("nav-quiz").classList.remove("active");
    loadBooks();
}

function showMindMap() {
    document.getElementById("upload-section").style.display = "none";
    document.getElementById("summary-section").style.display = "none";
    document.getElementById("books-section").style.display = "none";
    document.getElementById("mindmap-section").style.display = "block";
    document.getElementById("quiz-section").style.display = "none";
    document.getElementById("nav-mindmap").classList.add("active");
    document.getElementById("nav-upload").classList.remove("active");
    document.getElementById("nav-summary").classList.remove("active");
    document.getElementById("nav-books").classList.remove("active");
    document.getElementById("nav-quiz").classList.remove("active");
}

function showQuiz() {
    document.getElementById("upload-section").style.display = "none";
    document.getElementById("summary-section").style.display = "none";
    document.getElementById("books-section").style.display = "none";
    document.getElementById("mindmap-section").style.display = "none";
    document.getElementById("quiz-section").style.display = "block";
    document.getElementById("nav-quiz").classList.add("active");
    document.getElementById("nav-upload").classList.remove("active");
    document.getElementById("nav-summary").classList.remove("active");
    document.getElementById("nav-books").classList.remove("active");
    document.getElementById("nav-mindmap").classList.remove("active");
}

function goToSummary() {
    showSummary();
}

let allBooks = [];

async function loadBooks() {
    const res = await fetch("/my-books", {
        headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();
    allBooks = data;
    renderBooks(allBooks);
}

function renderBooks(books) {
    const list = document.getElementById("books-list");

    if (books.length === 0) {
        list.innerHTML = `<div class="books-empty">No books found.</div>`;
        return;
    }

    list.innerHTML = `
        <table class="table table-hover mb-0">
            <thead>
                <tr>
                    <th scope="col">Book ID</th>
                    <th scope="col">Book Name</th>
                    <th scope="col">Author</th>
                </tr>
            </thead>
            <tbody>
                ${books.map(book => `
                    <tr>
                        <td>B${book.book_id}</td>
                        <td>${book.title}</td>
                        <td>${book.author}</td>
                    </tr>
                `).join("")}
            </tbody>
        </table>
    `;
}

function filterBooks() {
    const query = document.getElementById("book-search").value.toLowerCase();
    const filtered = allBooks.filter(book =>
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query)
    );
    renderBooks(filtered);
}

async function uploadBook() {
    const inputType = getToggleValue("input-type-toggle");
    const uploadBtn = document.querySelector("#upload-section .btn-main");
    uploadBtn.disabled = true;
    uploadBtn.innerText = "Uploading...";

    let response;

    if (inputType === "file") {
        const title = document.getElementById("title").value;
        const author = document.getElementById("author").value;
        const file = document.getElementById("file").files[0];

        if (!title || !author || !file) {
            showToast("Please fill all fields and select a file", "danger");
            uploadBtn.disabled = false;
            uploadBtn.innerText = "Upload";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        response = await fetch(`/upload-book?title=${encodeURIComponent(title)}&author=${encodeURIComponent(author)}`, {
            method: "POST",
            headers: { "Authorization": "Bearer " + token },
            body: formData
        });

    } else {
        const text = document.getElementById("pasted-text").value.trim();
        if (!text) {
            showToast("Please paste some text", "danger");
            uploadBtn.disabled = false;
            uploadBtn.innerText = "Upload";
            return;
        }
        const formData = new FormData();
        formData.append("text", text);
        response = await fetch("/upload-pasted-text", {
            method: "POST",
            headers: { "Authorization": "Bearer " + token },
            body: formData
        });
    }

    const data = await response.json();
    uploadBtn.disabled = false;
    uploadBtn.innerText = "Upload";

    if (response.ok) {
        const id = inputType === "file" ? `B${data.book_id}` : data.pasted_id;
        document.getElementById("uploaded-id").innerText = id;
        document.getElementById("upload-result").style.display = "block";
        document.getElementById("book_id").value = id;
        document.getElementById("mindmap-book-id").value = id;
        document.getElementById("quiz-book-id").value = id;
        document.getElementById("goto-summary-btn").style.display = "inline-block";
    } else {
        showToast(data.detail || "Upload failed", "danger");
    }
}

let activeInterval = null;

function setToggle(groupId, btn) {
    const group = document.getElementById(groupId);
    group.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
}

function getToggleValue(groupId) {
    const group = document.getElementById(groupId);
    const active = group.querySelector(".toggle-btn.active");
    return active ? active.dataset.value : null;
}

async function generateSummary(force = false) {
    const bookId = document.getElementById("book_id").value;
    if (!bookId) {
        showToast("Please enter a Book ID", "danger");
        return;
    }

    const format = getToggleValue("format-toggle");
    const length = getToggleValue("length-toggle");

    if (format === "mindmap") {
        document.getElementById("mindmap-book-id").value = bookId;
        showMindMap();
        await generateMindMap();
        return;
    }

    const box = document.getElementById("summary-box");
    const text = document.getElementById("summary-text");
    const btn = document.getElementById("generate-btn");
    const regenBtn = document.getElementById("regenerate-btn");
    const historyBtn = document.getElementById("history-btn");
    const copyBtn = document.getElementById("copy-btn");
    const downloadBtn = document.getElementById("download-btn");
    const historyBox = document.getElementById("history-box");

    box.style.display = "block";
    historyBox.style.display = "none";
    btn.disabled = true;
    btn.innerText = "Processing...";
    regenBtn.style.display = "none";
    historyBtn.style.display = "none";
    copyBtn.style.display = "none";
    downloadBtn.style.display = "none";

    text.innerHTML = `<div style="font-size:0.875rem; color:#5a7357;" id="progress-label">Starting...</div>`;

    if (activeInterval) {
        clearInterval(activeInterval);
        activeInterval = null;
    }

    const kickoff = await fetch(`/generate-summary/${bookId}?format=${format}&length=${length}&force=${force}`, {
        method: "POST"
    });
    const kickoffData = await kickoff.json();

    if (kickoffData.status === "done") {
        text.innerText = kickoffData.summary;
        if (kickoffData.cached) showToast("Loaded from cache!", "success");
        else showToast("Summary ready!", "success");
        btn.disabled = false;
        btn.innerText = "Generate Summary";
        regenBtn.style.display = "inline-block";
        historyBtn.style.display = "inline-block";
        copyBtn.style.display = "inline-block";
        downloadBtn.style.display = "inline-block";
        return;
    }

    let pollCount = 0;
    const maxPolls = 500;

    activeInterval = setInterval(async () => {
        pollCount++;

        if (pollCount > maxPolls) {
            clearInterval(activeInterval);
            activeInterval = null;
            text.innerText = "Processing is taking longer than expected. Please wait a moment and try clicking Generate Summary again — it may load from cache.";
            btn.disabled = false;
            btn.innerText = "Generate Summary";
            showToast("Summary generation timed out", "danger");
            return;
        }

        const res = await fetch(`/summary-status/${bookId}`);
        const data = await res.json();

        if (data.status === "done") {
            clearInterval(activeInterval);
            activeInterval = null;
            text.innerText = data.summary;
            btn.disabled = false;
            btn.innerText = "Generate Summary";
            regenBtn.style.display = "inline-block";
            historyBtn.style.display = "inline-block";
            copyBtn.style.display = "inline-block";
            downloadBtn.style.display = "inline-block";
            showToast("Summary ready!", "success");
        } else {
            const pct = data.progress || 0;
            const label = document.getElementById("progress-label");
            if (label) {
                if (pct < 80) label.innerText = `Processing chunks... ${pct}%`;
                else if (pct < 100) label.innerText = `Combining summary... ${pct}%`;
                else label.innerText = "Finalizing...";
            }
        }
    }, 5000);
}

async function regenerateSummary() {
    const bookId = document.getElementById("book_id").value;
    if (!bookId) return;
    if (!confirm("Generate a new summary? The old one will still be saved in history.")) return;
    await generateSummary(true);
}

async function toggleHistory() {
    const bookId = document.getElementById("book_id").value;
    if (!bookId) {
        showToast("Please enter a Book ID", "danger");
        return;
    }

    const historyBox = document.getElementById("history-box");

    if (historyBox.style.display === "block") {
        historyBox.style.display = "none";
        return;
    }

    const res = await fetch(`/summary-history/${bookId}`, {
        headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();

    if (!res.ok) {
        showToast(data.detail, "danger");
        return;
    }

    const list = document.getElementById("history-list");
    list.innerHTML = data.map((s, i) => `
        <div class="history-item">
            <div class="history-version">
                Version ${s.version} ${i === 0 ? "(Latest)" : ""}
                <span style="margin-left:8px; font-size:0.65rem; background:rgba(61,92,58,0.1); color:var(--accent); padding:2px 8px; border-radius:10px; text-transform:uppercase; letter-spacing:0.06em;">
                    ${s.summary_type.replace("_", " · ")}
                </span>
            </div>
            <div class="history-text">${s.summary_text}</div>
        </div>
    `).join("");

    historyBox.style.display = "block";
}

function copySummary() {
    const text = document.getElementById("summary-text").innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast("Summary copied to clipboard!", "success");
    });
}

async function generateMindMap() {
    const bookId = document.getElementById("mindmap-book-id").value;
    if (!bookId) {
        showToast("Please enter a Book ID", "danger");
        return;
    }

    const container = document.getElementById("mindmap-container");
    const btn = document.querySelector("#mindmap-section .btn-main");

    container.innerHTML = "<p style='color:var(--muted); font-size:0.875rem; padding:16px;'>Generating mind map...</p>";
    btn.disabled = true;
    btn.innerText = "Generating...";

    const res = await fetch(`/mindmap/${bookId}`);
    const data = await res.json();

    btn.disabled = false;
    btn.innerText = "Generate Mind Map";

    if (!res.ok) {
        container.innerHTML = `<p style='color:var(--danger); padding:16px;'>${data.detail}</p>`;
        showToast(data.detail, "danger");
        return;
    }

    renderMindMap(data.mindmap);
    document.getElementById("export-mindmap-btn").style.display = "inline-block";
    showToast("Mind map ready!", "success");
}

function getColorScheme(type) {
    const t = (type || "").toLowerCase();
    if (t.includes("step") || t.includes("process") || t.includes("tutorial") || t.includes("how")) {
        return {
            root: "#2c4a7c", mid: "#4a72b0", leaf: "#d0dff5",
            stroke: { root: "#1e3560", mid: "#2c4a7c", leaf: "#7a9fd4" },
            text: { root: "white", mid: "white", leaf: "#1e2d4a" }
        };
    } else if (t.includes("hierarch") || t.includes("classif") || t.includes("categor") || t.includes("taxonom")) {
        return {
            root: "#6b3a7d", mid: "#9b5ab0", leaf: "#ead5f5",
            stroke: { root: "#4a2560", mid: "#6b3a7d", leaf: "#b07ac8" },
            text: { root: "white", mid: "white", leaf: "#2d1a3a" }
        };
    } else if (t.includes("timeline") || t.includes("history") || t.includes("event") || t.includes("chronolog")) {
        return {
            root: "#7c4a2c", mid: "#b07040", leaf: "#f5dfc0",
            stroke: { root: "#5c3018", mid: "#7c4a2c", leaf: "#d0a070" },
            text: { root: "white", mid: "white", leaf: "#2d1a0a" }
        };
    } else if (t.includes("compar") || t.includes("vs") || t.includes("contrast") || t.includes("differ")) {
        return {
            root: "#2c6b6b", mid: "#4a9b9b", leaf: "#c0eded",
            stroke: { root: "#1a4a4a", mid: "#2c6b6b", leaf: "#70baba" },
            text: { root: "white", mid: "white", leaf: "#0a2a2a" }
        };
    } else if (t.includes("cause") || t.includes("effect") || t.includes("impact") || t.includes("result")) {
        return {
            root: "#7c2c2c", mid: "#b04040", leaf: "#f5c0c0",
            stroke: { root: "#5c1818", mid: "#7c2c2c", leaf: "#d07070" },
            text: { root: "white", mid: "white", leaf: "#2d0a0a" }
        };
    } else {
        return {
            root: "#3d5c3a", mid: "#6b9467", leaf: "#ddeedd",
            stroke: { root: "#2e4a2b", mid: "#4a7046", leaf: "#9db89a" },
            text: { root: "white", mid: "white", leaf: "#1e2d1c" }
        };
    }
}

function renderMindMap(data) {
    const container = document.getElementById("mindmap-container");
    container.innerHTML = "";

    const type = data.type || "general";
    const scheme = getColorScheme(type);

    const width = container.offsetWidth || 900;
    const height = 750;

    const svg = d3.select("#mindmap-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("border-radius", "12px")
        .style("background", "#f4f7f3");

    svg.append("text")
        .attr("x", 12)
        .attr("y", 24)
        .style("font-size", "10px")
        .style("font-family", "DM Sans, sans-serif")
        .style("fill", "#5a7357")
        .style("font-weight", "600")
        .style("text-transform", "uppercase")
        .style("letter-spacing", "0.08em")
        .text(`◈ ${data.type || "General"}`);

    const g = svg.append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    svg.call(d3.zoom().scaleExtent([0.4, 2]).on("zoom", (event) => {
        g.attr("transform", event.transform);
    }));

    const root = d3.hierarchy(data);
    const radius = Math.min(width, height) / 2 - 20;

    const treeLayout = d3.tree()
        .size([2 * Math.PI, radius])
        .separation((a, b) => (a.parent == b.parent ? 4 : 5) / a.depth);

    treeLayout(root);

    const radialPoint = (x, y) => [
        y * Math.cos(x - Math.PI / 2),
        y * Math.sin(x - Math.PI / 2)
    ];

    root.each(d => {
        const p = radialPoint(d.x, d.y);
        d.px = p[0];
        d.py = p[1];
    });

    function getBoxSize(name, depth) {
        const words = name.split(" ");
        const isRoot = depth === 0;
        const charWidth = isRoot ? 7.5 : 6.5;
        const paddingX = 20;
        const paddingY = isRoot ? 14 : 12;
        const lines = [];
        for (let i = 0; i < words.length; i += 3) {
            lines.push(words.slice(i, i + 3).join(" "));
        }
        const longestLine = lines.reduce((a, b) => a.length > b.length ? a : b, "");
        const boxW = Math.max(longestLine.length * charWidth + paddingX, isRoot ? 100 : 80);
        const lineHeight = isRoot ? 16 : 14;
        const boxH = lines.length * lineHeight + paddingY;
        return { boxW, boxH, lines };
    }

    g.selectAll(".link")
        .data(root.links())
        .enter()
        .append("path")
        .attr("fill", "none")
        .attr("stroke", "#9db89a")
        .attr("stroke-width", 1.8)
        .attr("d", d => {
            const mx = (d.source.px + d.target.px) / 2;
            const my = (d.source.py + d.target.py) / 2;
            return `M${d.source.px},${d.source.py} Q${mx},${my} ${d.target.px},${d.target.py}`;
        });

    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter()
        .append("g")
        .attr("transform", d => `translate(${d.px}, ${d.py})`);

    node.each(function(d) {
        const el = d3.select(this);
        const isRoot = d.depth === 0;
        const isMid = d.depth === 1;

        const { boxW, boxH, lines } = getBoxSize(d.data.name, d.depth);

        const bgColor = isRoot ? scheme.root : isMid ? scheme.mid : scheme.leaf;
        const textColor = isRoot ? scheme.text.root : isMid ? scheme.text.mid : scheme.text.leaf;
        const strokeColor = isRoot ? scheme.stroke.root : isMid ? scheme.stroke.mid : scheme.stroke.leaf;
        const fontSize = isRoot ? "12px" : isMid ? "11px" : "10px";
        const fontWeight = isRoot ? "700" : isMid ? "600" : "400";
        const lineHeight = isRoot ? 16 : 14;

        el.append("rect")
            .attr("x", -boxW / 2)
            .attr("y", -boxH / 2)
            .attr("width", boxW)
            .attr("height", boxH)
            .attr("rx", 10)
            .attr("ry", 10)
            .attr("fill", bgColor)
            .attr("stroke", strokeColor)
            .attr("stroke-width", 1.5);

        const totalTextH = lines.length * lineHeight;
        const startY = -totalTextH / 2 + lineHeight / 2;

        lines.forEach((line, i) => {
            el.append("text")
                .attr("text-anchor", "middle")
                .attr("x", 0)
                .attr("y", startY + i * lineHeight)
                .attr("dominant-baseline", "middle")
                .style("font-size", fontSize)
                .style("font-family", "DM Sans, sans-serif")
                .style("fill", textColor)
                .style("font-weight", fontWeight)
                .style("pointer-events", "none")
                .text(line);
        });
    });
}

function exportMindMap() {
    const svg = document.querySelector("#mindmap-container svg");
    if (!svg) {
        showToast("No mind map to export", "danger");
        return;
    }

    const bookId = document.getElementById("mindmap-book-id").value || "mindmap";
    const width = parseInt(svg.getAttribute("width")) || 900;
    const height = parseInt(svg.getAttribute("height")) || 750;

    const cloned = svg.cloneNode(true);
    const style = document.createElementNS("http://www.w3.org/2000/svg", "style");
    style.textContent = `text { font-family: Arial, sans-serif; }`;
    cloned.insertBefore(style, cloned.firstChild);
    cloned.setAttribute("xmlns", "http://www.w3.org/2000/svg");

    const serializer = new XMLSerializer();
    const svgStr = serializer.serializeToString(cloned);
    const svgBlob = new Blob([svgStr], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);

    const canvas = document.createElement("canvas");
    canvas.width = width * 2;
    canvas.height = height * 2;
    const ctx = canvas.getContext("2d");
    ctx.scale(2, 2);
    ctx.fillStyle = "#f4f7f3";
    ctx.fillRect(0, 0, width, height);

    const img = new Image();
    img.crossOrigin = "anonymous";

    img.onload = function () {
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        const link = document.createElement("a");
        link.download = `mindmap_${bookId}.jpg`;
        link.href = canvas.toDataURL("image/jpeg", 0.95);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showToast("Mind map exported!", "success");
    };

    img.onerror = function () {
        URL.revokeObjectURL(url);
        showToast("Export failed — try the SVG option instead", "danger");
    };

    img.src = url;
}

let quizData = [];
let currentQuestion = 0;
let score = 0;
let userAnswers = [];

async function startQuiz() {
    const bookId = document.getElementById("quiz-book-id").value;
    if (!bookId) {
        showToast("Please enter a Book ID", "danger");
        return;
    }

    const btn = document.getElementById("quiz-generate-btn");
    btn.disabled = true;
    btn.innerText = "Generating...";

    const res = await fetch(`/quiz/${bookId}`);
    const data = await res.json();

    btn.disabled = false;
    btn.innerText = "Generate Quiz";

    if (!res.ok) {
        showToast(data.detail, "danger");
        return;
    }

    quizData = data.quiz;
    currentQuestion = 0;
    score = 0;
    userAnswers = [];

    document.getElementById("quiz-box").style.display = "block";
    document.getElementById("quiz-results-box").style.display = "none";
    document.getElementById("quiz-question-box").style.display = "block";

    renderQuestion();
    showToast("Quiz ready!", "success");
}

function renderQuestion() {
    const q = quizData[currentQuestion];
    const total = quizData.length;

    document.getElementById("quiz-progress").innerText = `Question ${currentQuestion + 1} of ${total}`;
    document.getElementById("quiz-question").innerText = q.question;
    document.getElementById("quiz-feedback").style.display = "none";
    document.getElementById("quiz-next-btn").style.display = "none";

    const optionsEl = document.getElementById("quiz-options");
    optionsEl.innerHTML = "";

    Object.entries(q.options).forEach(([key, value]) => {
        const btn = document.createElement("button");
        btn.className = "quiz-option";
        btn.innerText = `${key}. ${value}`;
        btn.onclick = () => selectAnswer(key, btn);
        optionsEl.appendChild(btn);
    });
}

function selectAnswer(selected, btnEl) {
    const q = quizData[currentQuestion];
    const correct = q.answer;
    const allOptions = document.querySelectorAll(".quiz-option");
    const feedback = document.getElementById("quiz-feedback");
    const nextBtn = document.getElementById("quiz-next-btn");

    allOptions.forEach(b => b.classList.add("disabled"));

    allOptions.forEach(b => {
        const key = b.innerText.split(".")[0];
        if (key === correct) b.classList.add("correct");
        else if (key === selected && selected !== correct) b.classList.add("wrong");
    });

    const isCorrect = selected === correct;
    if (isCorrect) score++;

    userAnswers.push({ question: q.question, selected, correct, options: q.options, isCorrect });

    feedback.style.display = "block";
    feedback.style.background = isCorrect ? "rgba(90,150,90,0.15)" : "rgba(192,98,90,0.12)";
    feedback.style.color = isCorrect ? "#2d5a2d" : "#7a2a25";
    feedback.style.border = `1px solid ${isCorrect ? "#5a9a5a" : "#c0625a"}`;
    feedback.innerText = isCorrect
        ? "✓ Correct!"
        : `✗ Wrong! The correct answer is ${correct}. ${q.options[correct]}`;

    if (currentQuestion < quizData.length - 1) {
        nextBtn.style.display = "inline-block";
    } else {
        nextBtn.style.display = "inline-block";
        nextBtn.innerText = "See Results →";
        nextBtn.onclick = showResults;
    }
}

function nextQuestion() {
    currentQuestion++;
    document.getElementById("quiz-next-btn").innerText = "Next →";
    document.getElementById("quiz-next-btn").onclick = nextQuestion;
    renderQuestion();
}

function showResults() {
    document.getElementById("quiz-question-box").style.display = "none";
    document.getElementById("quiz-results-box").style.display = "block";

    const total = quizData.length;
    const pct = Math.round((score / total) * 100);

    document.getElementById("quiz-score-display").innerText = `${score} / ${total}`;

    let msg = "";
    if (pct === 100) msg = "🎉 Perfect score! Excellent understanding!";
    else if (pct >= 80) msg = "👏 Great job! You know this book well.";
    else if (pct >= 60) msg = "👍 Good effort! Review the missed questions.";
    else if (pct >= 40) msg = "📖 Keep reading! Try again after reviewing.";
    else msg = "💪 Don't give up! Give the summary another read.";

    document.getElementById("quiz-score-msg").innerText = msg;

    const reviewEl = document.getElementById("quiz-review");
    reviewEl.innerHTML = userAnswers.map((a, i) => `
        <div class="review-item">
            <div class="review-question">Q${i + 1}. ${a.question}</div>
            <div class="review-answer ${a.isCorrect ? "correct" : "wrong"}">
                Your answer: ${a.selected}. ${a.options[a.selected]}
                ${!a.isCorrect ? `<br>Correct answer: ${a.correct}. ${a.options[a.correct]}` : ""}
            </div>
        </div>
    `).join("");
}

function toggleDarkMode() {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("darkMode", isDark ? "on" : "off");
    document.getElementById("dark-mode-btn").innerText = isDark ? "◑" : "◐";
}

async function loadProfile() {
    const res = await fetch("/me", {
        headers: { "Authorization": "Bearer " + token }
    });
    if (res.ok) {
        const data = await res.json();
        document.getElementById("profile-name").innerText = data.name;
        document.getElementById("profile-email").innerText = data.email;
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const bookId = document.getElementById("book_id").value;
    const summaryText = document.getElementById("summary-text").innerText;
    const format = getToggleValue("format-toggle");
    const length = getToggleValue("length-toggle");

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("Summarium", 20, 20);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(11);
    doc.setTextColor(90, 115, 87);
    doc.text(`Book ID: ${bookId}  |  Format: ${format}  |  Length: ${length}`, 20, 30);

    doc.setDrawColor(90, 115, 87);
    doc.setLineWidth(0.5);
    doc.line(20, 35, 190, 35);

    doc.setFont("helvetica", "bold");
    doc.setFontSize(13);
    doc.setTextColor(30, 45, 28);
    doc.text("Summary", 20, 45);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(50, 50, 50);

    const lines = doc.splitTextToSize(summaryText, 170);
    let y = 55;
    const pageHeight = doc.internal.pageSize.height;

    lines.forEach(line => {
        if (y > pageHeight - 20) {
            doc.addPage();
            y = 20;
        }
        doc.text(line, 20, y);
        y += 6;
    });

    doc.setFontSize(8);
    doc.setTextColor(150, 150, 150);
    doc.text(`Generated by Summarium | ${new Date().toLocaleDateString()}`, 20, pageHeight - 10);

    doc.save(`summary_book_${bookId}.pdf`);
    showToast("PDF downloaded!", "success");
}

function toggleProfile() {
    const dropdown = document.getElementById("profile-dropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

document.addEventListener("click", (e) => {
    const wrap = document.getElementById("profile-wrap");
    if (wrap && !wrap.contains(e.target)) {
        const dropdown = document.getElementById("profile-dropdown");
        if (dropdown) dropdown.style.display = "none";
    }
});

function logout() {
    localStorage.clear();
    window.location.href = "/app";
}

window.addEventListener("DOMContentLoaded", async () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark");
    }

    if (token) {
        const role = localStorage.getItem("userRole");
        if (role === "admin") return;

        const res = await fetch("/verify-token", {
            headers: { "Authorization": "Bearer " + token }
        });
        if (res.ok) {
            document.getElementById("auth-section").style.display = "none";
            document.getElementById("dashboard").style.display = "block";
            showUpload();
            await loadProfile();
        } else {
            token = "";
            localStorage.removeItem("token");
            localStorage.removeItem("userRole");
        }
    }
});