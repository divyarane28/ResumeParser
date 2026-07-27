const resumeInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");
const uploadBtn = document.getElementById("upload-btn");

resumeInput.addEventListener("change", () => {

    if (resumeInput.files.length > 0)
        fileName.textContent = resumeInput.files[0].name;
    else
        fileName.textContent = "No file selected";

});

uploadBtn.addEventListener("click", async () => {

    if (resumeInput.files.length === 0) {

        alert("Select Resume");
        return;

    }

    const formData = new FormData();
    formData.append("file", resumeInput.files[0]);

    const response = await fetch("/upload", {

        method: "POST",
        body: formData

    });

    const result = await response.json();

    const data = result.parsed_data;

    document.getElementById("name").value = data.name || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("phone").value = data.phone || "";

    document.getElementById("skills").value =
        (data.skills || []).join("\n");

    document.getElementById("education").value =
    (data.education || [])
    .map(item => {

        if (typeof item === "string")
            return item;

        return `${item.degree || ""} ${item.field || ""}
        ${item.university || ""}
        ${item.year || ""}`;

        })
        .join("\n\n");

    document.getElementById("experience").value =
    (data.experience || [])
    .map(job => {

        return `Role: ${job.role || job.title || ""}
Company: ${job.company || ""}
Duration: ${job.duration || ""}`;

    })
    .join("\n\n---------------------\n\n");

});

const submitBtn = document.getElementById("submit-btn");

submitBtn.addEventListener("click", () => {

    const candidate = {

        name: document.getElementById("name").value,

        email: document.getElementById("email").value,

        phone: document.getElementById("phone").value,

        skills: document.getElementById("skills").value,

        education: document.getElementById("education").value,

        experience: document.getElementById("experience").value

    };

    localStorage.setItem("candidate", JSON.stringify(candidate));

    window.location.href = "/candidate";

});