const statusBox = document.getElementById("status");
const solutionBox = document.getElementById("solution");

const API_BASE = "http://127.0.0.1:8000"; // backend address

let isBusy = false; // prevent double clicks

function updateStatus(msg) {
    statusBox.textContent = msg;
}

// -------------------- SCAN FACE --------------------
async function scanFace(face) {
    if (isBusy) return;
    isBusy = true;

    updateStatus(`📷 Scanning face ${face}...`);

    try {
        const imageBlob = await captureFrame();

        if (!imageBlob) {
            throw new Error("Camera capture failed");
        }

        const formData = new FormData();
        formData.append("face", face);
        formData.append("image", imageBlob, "face.jpg");

        const response = await fetch(`${API_BASE}/scan_face`, {
            method: "POST",
            body: formData
        });

        const text = await response.text(); // IMPORTANT
        let data = {};

        try {
            data = JSON.parse(text);
        } catch {
            throw new Error("Invalid server response");
        }

        if (!response.ok || data.error) {
            throw new Error(data.error || `Server error (${response.status})`);
        }

        updateStatus(
            `✅ Face ${face} scanned successfully\n` +
            `Scanned: ${data.faces_scanned.join(", ")}`
        );

    } catch (err) {
        console.error(err);
        updateStatus(`❌ Scan failed: ${err.message}`);
    } finally {
        isBusy = false;
    }
}

// -------------------- SOLVE CUBE --------------------
async function solveCube() {
    if (isBusy) return;
    isBusy = true;

    updateStatus("🧠 Solving cube...");
    solutionBox.textContent = "";

    try {
        const response = await fetch(`${API_BASE}/solve`, {
            method: "POST"
        });

        const text = await response.text();
        let data = {};

        try {
            data = JSON.parse(text);
        } catch {
            throw new Error("Invalid server response");
        }

        if (!response.ok || data.error) {
            throw new Error(data.error || `Server error (${response.status})`);
        }

        updateStatus("🎉 Cube solved successfully!");

        if (Array.isArray(data.solution)) {
            solutionBox.textContent = data.solution.join(" ");
        } else {
            solutionBox.textContent = data.solution;
        }

    } catch (err) {
        console.error(err);
        updateStatus(`❌ Solve failed: ${err.message}`);
    } finally {
        isBusy = false;
    }
}

// -------------------- RESET --------------------
async function resetCube() {
    if (isBusy) return;
    isBusy = true;

    try {
        const response = await fetch(`${API_BASE}/reset`, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Reset failed");
        }

        updateStatus("🔄 Scan reset. Ready to scan cube.");
        solutionBox.textContent = "";

    } catch (err) {
        console.error(err);
        updateStatus(`❌ Reset failed: ${err.message}`);
    } finally {
        isBusy = false;
    }
}
