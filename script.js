console.log("SCRIPT.JS LOADED");

let parsedResumeData = null;
let parsedJDData = null;
let resumeText = "";

const resumeInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");
const uploadBtn = document.getElementById("upload-btn");
const loadingMessage = document.getElementById("loading-message");

console.log("SCRIPT LOADED");
console.log("Loading element:", loadingMessage);

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

    // Show processing message
    loadingMessage.style.display = "block";
    loadingMessage.textContent = "⏳ Parsing resume... Please wait.";

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Processing...";

    const formData = new FormData();
    formData.append("file", resumeInput.files[0]);

    await new Promise(resolve => setTimeout(resolve, 100));

    const response = await fetch("/upload", {

    method: "POST",
    body: formData

    });

    const result = await response.json();

    const data = result.parsed_data;
    parsedResumeData = data;
    resumeText = result.resume_text || "";

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

    // Parsing completed
    loadingMessage.style.display = "none";

    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload Resume";

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

const matchJdBtn = document.getElementById("match-jd-btn");
const jdLoadingMessage = document.getElementById("jd-loading-message");

matchJdBtn.addEventListener("click", async () => {

    const jdText = document.getElementById("job-description").value;

    if (jdText.trim() === "") {

        alert("Please paste a Job Description.");

        return;
    }

    if (!parsedResumeData) {

        alert("Please upload and parse a resume first.");

        return;
    }

    jdLoadingMessage.style.display = "block";

    matchJdBtn.disabled = true;
    matchJdBtn.textContent = "Analyzing...";

    // Step 1: Analyze Job Description

    const response = await fetch("/analyze-jd", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            job_description: jdText
        })

    });

    const result = await response.json();

    console.log("JD Analysis Result:");
    console.log(result);

    // Store parsed JD

    parsedJDData = result.parsed_jd;

    // Step 2: Match Resume with JD

    const matchResponse = await fetch("/match", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            resume_data: parsedResumeData,
            resume_text: resumeText,
            jd_data: parsedJDData

        })

    });

    const matchResult = await matchResponse.json();

    console.log("FINAL MATCH RESULT:");
console.log(matchResult);


// Show match result

document.getElementById("match-result").style.display = "block";

const matchPercentage =
    document.getElementById("match-percentage");

const percentage = matchResult.match_percentage || 0;

matchPercentage.textContent = percentage + "%";

if (percentage < 40) {

    matchPercentage.style.color = "#dc2626";

} else if (percentage < 70) {

    matchPercentage.style.color = "#f59e0b";

} else {

    matchPercentage.style.color = "#16a34a";

}


// Matching required skills

const matchedSkills =
    document.getElementById("matched-skills");

if (
    matchResult.matched_required_skills &&
    matchResult.matched_required_skills.length > 0
) {

    matchedSkills.textContent =
        matchResult.matched_required_skills.join(", ");

} else {

    matchedSkills.textContent =
        "No matching required skills";

}


// Missing required skills

const missingSkills =
    document.getElementById("missing-skills");

if (
    matchResult.missing_required_skills &&
    matchResult.missing_required_skills.length > 0
) {

    missingSkills.textContent =
        matchResult.missing_required_skills.join(", ");

} else {

    missingSkills.textContent =
        "No missing required skills";

}


// Matching preferred skills

const preferredSkills =
    document.getElementById("matched-preferred-skills");

if (
    matchResult.matched_preferred_skills &&
    matchResult.matched_preferred_skills.length > 0
) {

    preferredSkills.textContent =
        matchResult.matched_preferred_skills.join(", ");

} else {

    preferredSkills.textContent =
        "No matching preferred skills";

}
jdLoadingMessage.style.display = "none";

matchJdBtn.disabled = false;
matchJdBtn.textContent = "🔍 Match Resume with JD";

});