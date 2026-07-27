const candidate = JSON.parse(localStorage.getItem("candidate"));

if(candidate){

    document.getElementById("candidate-name").textContent =
        candidate.name;

    document.getElementById("candidate-email").textContent =
        candidate.email;

    document.getElementById("candidate-phone").textContent =
        candidate.phone;

    // Skills

    const skills=document.getElementById("candidate-skills");

    skills.innerHTML="";

    candidate.skills.split("\n").forEach(skill=>{

        if(skill.trim()!=""){

            const div=document.createElement("div");

            div.className="skill-chip";

            div.textContent=skill;

            skills.appendChild(div);

        }

    });

    // Education

    document.getElementById("candidate-education").innerHTML=
        "<div class='card'>"+candidate.education.replace(/\n/g,"<br>")+"</div>";

    // Experience

    document.getElementById("candidate-experience").innerHTML=
        "<div class='card'>"+candidate.experience.replace(/\n/g,"<br>")+"</div>";

}