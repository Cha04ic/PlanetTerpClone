const courseInput = document.getElementById("courseInput0");
const courseDropdown = document.getElementsByClassName("dropdown")[1];
let courseData = [];
const profInput = document.getElementById("profInput0");
const profDropdown = document.getElementsByClassName("dropdown")[2];
let profData = [];
let selectedCourse = null;
let selectedProfessor = null;
let selectedItem = null;
let gradeChart;
let combinedData = [];
const combinedInput = document.getElementById("combinedInput");
const combinedDropdown = document.getElementsByClassName("dropdown")[0];
let searchButton = document.getElementById("search-button");
let isHome = false;  
    
combinedInput.addEventListener("input", function() {
    const query = combinedInput.value.toLowerCase();
    combinedDropdown.innerHTML = "";
    const filteredItems = combinedData.filter(item => item.name.toLowerCase().includes(query));
    if (filteredItems.length > 0) {
        combinedDropdown.style.display = "block";
        filteredItems.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item.name;
            li.classList.add("dropdown-item");
            li.addEventListener("click", function() {
                combinedInput.value = item.name;
                selectedItem = item.name;
                combinedDropdown.style.display = "none";
                isHome = true;
            });
            combinedDropdown.appendChild(li);
            });
    } else {
        combinedDropdown.style.display = "none";
    }
});

searchButton.addEventListener("click", function() {
    fetchGradeDistribution();
})

fetch("courses/")
    .then(response => response.json())
    .then(data => {
        courseData = data;
        updateCombinedData();
    }).catch(error => console.error("Error fetching courses: ", error));

fetch("profs/")
    .then(response => response.json())
    .then(data => {
        profData = data;
        updateCombinedData();
    }).catch(error => console.error("Error fetching professors: ", error));

function updateCombinedData() {
    if (courseData.length > 0 && profData.length > 0) {
        combinedData = [...courseData, ...profData];
    }
}

courseInput.addEventListener("input", function() {
    selectedCourse = null;
    const query = courseInput.value.toLowerCase();
    courseDropdown.innerHTML = "";
    const filteredCourses = courseData.filter(course => course.name.toLowerCase().includes(query));
    if (filteredCourses.length > 0) {
        courseDropdown.style.display = "block";
        filteredCourses.sort((a, b) => {
            return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        }).forEach(course => {
            const li = document.createElement("li");
            li.textContent = course.name;
            li.classList.add("dropdown-item");
            li.addEventListener("click", function () {
                courseInput.value = course.name;
                selectedCourse = course.name;
                courseDropdown.style.display = "none";
                fetchGradeDistribution();
            });
            courseDropdown.appendChild(li);
        })
    } else {
        courseDropdown.style.display = "none";
    }
});

profInput.addEventListener("input", function() {
    selectedProfessor = null;
    const query = profInput.value.toLowerCase();
    profDropdown.innerHTML = "";
    const filteredProfs = profData.filter(prof => prof.name.toLowerCase().includes(query));
    if (filteredProfs.length > 0) {
        profDropdown.style.display = "block";
        filteredProfs.forEach(prof => {
            const li = document.createElement("li");
            li.textContent = prof.name;
            li.classList.add("dropdown-item");
            console.log("b");
            li.addEventListener("click", function() {
                profInput.value = prof.name;
                selectedProfessor = prof.name;
                profDropdown.style.display = "none";
                fetchGradeDistribution();
            });
            profDropdown.appendChild(li);
        });
    } else {
        profDropdown.style.display = "none";
    }
});


// Hide dropdown when clicking outside
document.addEventListener("click", function(e) {
    if (!courseInput.contains(e.target) || !profInput.contains(e.target) || !combinedInput.contains(e.target)) {
        courseDropdown.style.display = "none";
        profDropdown.style.display = "none";
        combinedDropdown.style.display = "none";
    }
});


function fetchGradeDistribution() {
    let queryParams = [];
    const isCourse = courseData.some(course => course.name === selectedItem);
    if (isHome) {
        console.log("hi");
        queryParams.push(
            `${(isCourse) ? 'course' : 'professor'}=${encodeURIComponent(selectedItem)}`
        );
    } else {
        console.log("hello");
        if (selectedCourse) queryParams.push(`course=${encodeURIComponent(selectedCourse)}`);
        if (selectedProfessor) queryParams.push(`professor=${encodeURIComponent(selectedProfessor)}`);
    }

    const url = `grades/?${queryParams.join("&")}`;
    console.log(url);
    
    fetch(url)
        .then(response => response.json())
        .then(gradeData => {
            renderChart(gradeData);
        }).catch(error => console.error("Error fetching grades: ", error));
}

function renderChart(gradeData) {
    if (gradeChart) {
        gradeChart.destroy();
    }
    const ctx = (isHome ? document.getElementsByClassName("gradeChart")[0].getContext("2d") : 
                    document.getElementsByClassName("gradeChart")[1].getContext("2d"));

    isHome = false;
    selectedItem = null;

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
                    label: "-",
                    data: minusData,
                    backgroundColor: "rgba(20, 152, 152, 0.8)",
                },
                {
                    label: "Regular",
                    data: regularData,
                    backgroundColor: "rgba(18, 209, 209, 0.82)",
                },
                {
                    label: "+",
                    data: plusData,
                    backgroundColor: "rgba(20, 173, 171, 0.5)",
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
                    position: "top",
                    labels: {
                        generateLabels: function(chart) {
                            const originalLabels = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                            // Reorder legend items as needed
                            return [
                                originalLabels.find(label => label.text === "+"),
                                originalLabels.find(label => label.text === "Regular"),
                                originalLabels.find(label => label.text === "-"),
                                originalLabels.find(label => label.text === "F"),
                                originalLabels.find(label => label.text === "W"),
                                originalLabels.find(label => label.text === "Other"),
                            ];
                        }
                    }
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