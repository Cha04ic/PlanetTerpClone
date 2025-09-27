// Fetch course data from Django backend
fetch("courses/")
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        //console.log(data.length)
        courseData = data;
    })
    .catch(error => console.error("Error fetching courses:", error));

courseInput.addEventListener("input", function() {
    const query = courseInput.value.toLowerCase();  
    courseDropdown.innerHTML = "";  // Clear previous results
    const filteredCourses = courseData.filter(course => course.name.toLowerCase().includes(query));
    if (filteredCourses.length > 0) {
        courseDropdown.style.display = "block";
        filteredCourses.sort((a, b) => {
        // Ensure `a.name` and `b.name` are strings for comparison
        return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        })
        .forEach(course => {
            const li = document.createElement("li");
            li.textContent = course.name;
            li.classList.add("dropdown-item");
            li.addEventListener("click", function() {
            courseInput.value = course.name;  // Set input value on click
            courseDropdown.style.display = "none";
            displayGradeDistribution(course.name);
            });
            courseDropdown.appendChild(li);
        });
    } else {
        courseDropdown.style.display = "none";
    }
});

// Hide dropdown when clicking outside
document.addEventListener("click", function(e) {
    if (!courseInput.contains(e.target)) {
        courseDropdown.style.display = "none";
    }
});

function displayGradeDistribution(courseName) {
    fetch(`grades/?course=${courseName}`)
        .then(response => response.json())
        .then(gradeData => {
            console.log("Grade Data: ", gradeData);
            renderChart(gradeData);
        }).catch(error => console.error("Error fetching grades: ", error));
}

function renderChart(gradeData) {
    if (gradeChart) {
        gradeChart.destroy();
    }

    const ctx = document.getElementById("gradeChart").getContext("2d");

    const labels = ["A", "B", "C", "D", "F", "W", "Other"];

    const aggregateGrades = (gradeData, key) => {
        return gradeData.reduce((sum, grade) => sum + (grade[key] || 0), 0);
    };

    // Aggregate data for the chart
    const plusData = [
        aggregateGrades(gradeData, 'a_plus'),
        aggregateGrades(gradeData, 'b_plus'),
        aggregateGrades(gradeData, 'c_plus'),
        aggregateGrades(gradeData, 'd_plus'),
        0, 0, 0
    ];

    const regularData = [
        aggregateGrades(gradeData, 'a'),
        aggregateGrades(gradeData, 'b'),
        aggregateGrades(gradeData, 'c'),
        aggregateGrades(gradeData, 'd'),
        0, 0, 0
    ];

    const minusData = [
        aggregateGrades(gradeData, 'a_minus'),
        aggregateGrades(gradeData, 'b_minus'),
        aggregateGrades(gradeData, 'c_minus'),
        aggregateGrades(gradeData, 'd_minus'),
        0, 0, 0
    ];

    const fData = [0, 0, 0, 0, aggregateGrades(gradeData, 'f'), 0, 0];
    const wData = [0, 0, 0, 0, 0, aggregateGrades(gradeData, 'w'), 0];
    const otherData = [0, 0, 0, 0, 0, 0, aggregateGrades(gradeData, 'other')];

    gradeChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "+",
                    data: plusData,
                    backgroundColor: "rgba(75, 192, 192, 0.8)",
                },
                {
                    label: "Regular",
                    data: regularData,
                    backgroundColor: "rgba(75, 192, 192, 0.5)",
                },
                {
                    label: "-",
                    data: minusData,
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                },
                {
                    label: "F",
                    data: fData,
                    backgroundColor: "rgba(177, 11, 11, 0.6)",
                },
                {
                    label: "W",
                    data: wData,
                    backgroundColor: "rgba(255, 99, 132, 0.6)",
                },
                {
                    label: "Other",
                    data: otherData,
                    backgroundColor: "rgba(201, 203, 207, 0.6)",
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: "index",
                    intersect: false
                },
                legend: {
                    position: "top"
                }
            },
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            }
        }
    });
}





