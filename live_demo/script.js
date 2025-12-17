// Define available objects (could also be fetched via an API)
const availableObjects = ["cell phone", "phone", "bottle"];

window.onload = function() {
  const container = document.getElementById("checklist-container");
  // Clear any existing content
  container.innerHTML = '';
  
  availableObjects.forEach(obj => {
    // Create a label and checkbox for each object
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = "objects";
    checkbox.value = obj;
    
    // Pre-check if the object is in the currentSelectedObjects list
    if (currentSelectedObjects.includes(obj)) {
      checkbox.checked = true;
    }
    
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(" " + obj.charAt(0).toUpperCase() + obj.slice(1)));
    container.appendChild(label);
    container.appendChild(document.createElement("br"));
  });
};