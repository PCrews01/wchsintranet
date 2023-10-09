function alerters(id) {
  let i = $("#me");
  console.log("i, i", i);
  console.log("OOOHHHH", id);
  $.getJSON(`/show_form/${id}`, (data) => {
    console.log("EX", data);
  });
  return false;
}
() => {
  console.log(" YO");
};
function showSection(section) {
  let section_card = document.querySelector(`#${section}_card`);
  let section_title = document.querySelector(`#${section}_title`);
  let section_children = document.querySelector(`#${section}_children`);
  let section_toggler = document.querySelector(`#${section}_toggler`);

  section_card.scrollIntoView();

  if (section_title.style.marginTop == `${30}%`) {
    section_title.style.marginTop = `${0}%`;
    section_title.style.width = `${100}%`;

    section_card.style.minHeight = `${60}dvh`;

    section_children.style.height = `${60}%`;
    section_children.style.opacity = 1;

    section_toggler.innerText =
      section === "drive" ? `Hide my my ${section}` : `Hide all ${section}`;
  } else {
    // section_title.style.width = `${50}%`
    section_title.style.marginTop = `${30}%`;
    section_title.style.width = `${40}%`;

    section_card.style.minHeight = `${30}dvh`;

    section_children.style.height = `${0}%`;
    section_children.style.opacity = 0;

    section_toggler.innerText =
      section === "drive" ? `Show my ${section}` : `See all ${section}`;
  }
}

function drawCard(title, children) {
  let div = document.createElement("div");
  let header = document.createElement("h1");

  header.innerText("Draw Card");
  div.appendChild(header);
  return div;
}

function filterUser() {
  const form_input = document.querySelector("#people_search").value;
  const user_list = document.querySelector("#user_list").children;
  const user_group = document.querySelector("#user_list");

  let filtered_list = Array.from(user_list).filter((a) => {
    return a.firstElementChild.id.includes(
      form_input.replace(" ", "_").toLowerCase()
    );
  });

  for (u_item of user_list) {
    console.log("U It ", u_item);
    if (filtered_list.includes(u_item)) {
      u_item.classList.add("a-fade-in");
      u_item.classList.remove("hidden");
    } else {
      u_item.classList.add("hidden");
      u_item.classList.remove("a-fade-in");
    }
  }
}

function extendResults(n) {
  alert(n);
  fetch("");
}

function checkForStudentEmail(str) {
  return /\d/.test(str);
}

function checkedButton(e) {
  let student_emails = document.querySelectorAll(".student-ph");

  for (s_e of student_emails) {
    if (e.checked) {
      s_e.classList.remove("student-btn");
      s_e.classList.add("slide-up");
    } else {
      s_e.classList.add("student-btn");
      s_e.classList.remove("slide-up");
    }
  }
}

const doc_paths = ["get-sheets", "get-forms", "get-drive", "get-docs"];
function checker() {
  let a_el = document.createElement("a");
  let div_el = document.createElement("div");
  let u_list = document.querySelector("#user_list");
  let student_toggle = document.querySelector("#student_toggle");

  let loader = document.querySelector("#loader");
  let user_group = [];
  let local_people = JSON.parse(localStorage.getItem("people"))

  if(JSON.parse(localStorage.getItem("people")) && JSON.parse(localStorage.getItem("people")).length > 1){
    console.log(" Ready fi people")

    for (user of local_people) {
      if(!my_people.includes(user)){
        my_people.push(user)
      }
      let card_holder = document.createElement("a");
      let card_container = document.createElement("div");
      let card_body = document.createElement("div");
      let card_row = document.createElement("div");
      let card_col = document.createElement("div");
      let email_label = document.createElement("div");
      let email_column = document.createElement("div");
      let ou_label = document.createElement("div");
      let ou_column = document.createElement("div");
      let card_header = document.createElement("div");

      card_holder.href = `/users/${user.id}`;
      card_holder.classList.add("col-3", "slide-up");
      card_holder.id = student_toggle.checked
        ? `student_btn_${user.id}`
        : `card_body_${user.id}`;
      if (checkForStudentEmail(user.primaryEmail)) {
        card_holder.classList.add("student-btn", "student-ph");
      }

      card_container.classList.add(
        "card",
        "border-warning",
        "text-main",
        "mb-3"
      );
      card_container.id = `${user.primaryEmail}_${user.name.fullName
        .replace(" ", "_")
        .toLowerCase()}`;

      card_header.classList.add("card-header", "fs-2v");

      card_body.classList.add("card-body");

      card_row.classList.add("row");

      card_col.classList.add("col-3");

      email_label.classList.add("col-4");

      email_column.classList.add("col-8");

      ou_label.classList.add("col-4");

      ou_column.classList.add("col-8");

      card_header.innerText = user.name.fullName;

      email_column.innerText = user.primaryEmail;
      email_label.innerText = "Email: ";

      ou_column.innerText = user.orgUnitPath;
      ou_label.innerText = "OU: ";

      card_container.appendChild(card_header);
      card_container.appendChild(card_body);
      card_body.appendChild(card_row);

      card_holder.appendChild(card_container);

      card_row.appendChild(email_label);
      card_row.appendChild(email_column);
      card_row.appendChild(ou_label);
      card_row.appendChild(ou_column);

      u_list.appendChild(card_holder);

      loader.classList.add("a-fade-out", "o-0", "ht-0");
    }
  } else {
  fetch("/get-users").then((u) => {
    u.json().then((n) => {
      for (user of n) {
        if(!my_people.includes(user)){
          my_people.push(user)
        }
        let card_holder = document.createElement("a");
        let card_container = document.createElement("div");
        let card_body = document.createElement("div");
        let card_row = document.createElement("div");
        let card_col = document.createElement("div");
        let email_label = document.createElement("div");
        let email_column = document.createElement("div");
        let ou_label = document.createElement("div");
        let ou_column = document.createElement("div");
        let card_header = document.createElement("div");

        card_holder.href = `/users/${user.id}`;
        card_holder.classList.add("col-3", "slide-up");
        card_holder.id = student_toggle.checked
          ? `student_btn_${user.id}`
          : `card_body_${user.id}`;
        if (checkForStudentEmail(user.primaryEmail)) {
          card_holder.classList.add("student-btn", "student-ph");
        }

        card_container.classList.add(
          "card",
          "border-warning",
          "text-main",
          "mb-3"
        );
        card_container.id = `${user.primaryEmail}_${user.name.fullName
          .replace(" ", "_")
          .toLowerCase()}`;

        card_header.classList.add("card-header", "fs-2v");

        card_body.classList.add("card-body");

        card_row.classList.add("row");

        card_col.classList.add("col-3");

        email_label.classList.add("col-4");

        email_column.classList.add("col-8");

        ou_label.classList.add("col-4");

        ou_column.classList.add("col-8");

        card_header.innerText = user.name.fullName;

        email_column.innerText = user.primaryEmail;
        email_label.innerText = "Email: ";

        ou_column.innerText = user.orgUnitPath;
        ou_label.innerText = "OU: ";

        card_container.appendChild(card_header);
        card_container.appendChild(card_body);
        card_body.appendChild(card_row);

        card_holder.appendChild(card_container);

        card_row.appendChild(email_label);
        card_row.appendChild(email_column);
        card_row.appendChild(ou_label);
        card_row.appendChild(ou_column);

        u_list.appendChild(card_holder);

        loader.classList.add("a-fade-out", "o-0", "ht-0");
      }
      localStorage.setItem("people", JSON.stringify(my_people))
    });
  });
}

  for (path of doc_paths) {
    let named_item = path.replace("get-", "");
    // console.log("getter ", named_item);

    let my_list = getList(named_item)
    let local = localStorage.getItem(named_item)
    let parsed_local = JSON.parse(local)

    if(JSON.parse(local).length > 1){
      console.log(" I exist", typeof(parsed_local))
      for(j_item of parsed_local){
        console.log(" parsed ", j_item)
      }
    } else {

    
    fetch(`/${path}`).then((response) => {
      response.json().then((results) => {
        // console.log(named_item, results);

        for (res_item of results) {

        if(!my_list.includes(res_item)){
          my_list.push(res_item)
        }

          let item_container = document.createElement("div");
          let item_link = document.createElement("a");
          let item_card = document.createElement("div");
          let parent_container = document.querySelector(
            `#${named_item}_container`
          );

          item_container.classList.add(
            "col-md-6",
            "col-lg-4",
            "col-sm-6",
            "col-xs-12"
          );

          
          item_link.href = `https://docs.google.com/${getName(named_item)}/d/${res_item.id}/${named_item === "forms" ? "viewform" : ""}`
          item_link.target = `${named_item}-${res_item.id}`
          item_link.onclick = `window.open(${this.href},"Item Viewer", "popup")`

          item_card.classList.add(
            "card",
            "card-body",
            "mb-3",
            "slide-right",
            "text-dark"
          );

          item_card.innerText = res_item.name;
          item_link.appendChild(item_card);
          item_container.appendChild(item_link);

          parent_container.appendChild(item_container);
        }
        let dd = JSON.stringify(my_list)

        // console.log("DD ", dd)
        localStorage.setItem(named_item, dd)

      });
    });
    }
    let stripped_string = JSON.parse(localStorage.getItem(named_item))

  console.log("stripped", stripped_string)
    // localStorage.getItem(named_item).replace('[', '').replace(']', '').replace('},', "},---")
    // let grouped_string = stripped_string.split("---")

    // for(key of grouped_string){
    //   console.log("Key ", key)
    // }

    // console.log(" This is local ", grouped_string)
  }
}

  let ran = false
function openDocument(kind,id){

  const window_feature = "left=100,top=100,width=720,height=1020"
  const window_handle = window.open(`https://docs.google.com/${kind}/d/e/${id}/${kind === "forms" ? "viewform" : ""}`,"Item Viewer",window_feature, "popup")

  if(!window_handle && !ran){
    //window is not allowed to open
    alert("Hey, the window is unable to open.")
    ran = true
  }

}

function getName(name){
  if(name === "sheets"){
    return "spreadsheets"
  } else if(name === "docs"){
    return "document"
  } else if(name === "forms"){
    return "forms"
  } else if(name === "drive"){
    return "documents"
  }
}

let my_forms = []
let my_docs = []
let my_sheets = []
let my_drive = []
let my_people = []

function getList(named_item){
  if(named_item === "forms"){
    return my_forms
  } else if(named_item === "docs"){
    return my_docs
  } else if(named_item === "sheets"){
    return my_sheets
  } else if(named_item === "people"){
    return my_people
  } else if(named_item === "drive"){
    return my_drive
  } else {
    return []
  }
}

function clearCredentials(){
  localStorage.clear()
}

function setPage(title){
  let pill = document.querySelector("#home_pill")

  pill.classList.add('bg-light','text-main', 'rounded-5')

}

function getStaff(){
  let user_list = document.querySelector("#user_list").children
  if(user_list.length < 1){
    $.getJSON("/get-users").then((c) => {
      console.log("This is c", c)
    })
    .finally(() => {
      setPage("staff")
    })
  }
}
// pass the person and the page target - should be the element id
function createUserCard(person, target){
  
  let card_wrapper = document.createElement("div")

  let card_header = document.createElement("div")
  card_header.classList.add("card-header")
  card_header.textContent = `${person.first_name} ${person.last_name}`

  let card_body = document.createElement("div")
  card_body.className = "card-body ht-100p"

  let card_row = document.createElement("div")
  card_row.className = "row ht-90p"

  let card_image = document.createElement("img")
  card_image.classList = "ht-20d rounded-2 m-auto w-90p"
  card_image.setAttribute("src", person.thumbnail_url)

  let card_list = document.createElement("div")
  card_list.classList.add("row")
    
  let card_col_1 = document.createElement("div")
  card_col_1.classList.add("col-4")
  card_col_1.appendChild(card_image)

  let card_col_2 = document.createElement("div")
  card_col_2.className = "col-8 y-scroll ht-90p"
  card_col_2.appendChild(card_list)


  let card_list_row = document.createElement("div")
  card_list_row.classList.add("row")
  
  let target_element = document.querySelector(`#${target}`)

  // add classes to the elements
  card_wrapper.classList.add("card","bg-light","rounded-3","ht-30d","w-80p","o-hidden","m-auto","slide-up","slow-t","ar-16")
  
  // add attributes to elements
  // card_overlay.setAttribute("style", "margin: -20px 0 0 -20px;")

  // add text to elements

  // build the card

  for (const key in person){
    let label = document.createElement("small")
    label.setAttribute("style", "font-weight:bold;")
    label.textContent = `${key}:`

    let val = document.createElement("div")
    val.textContent = person[key]
    
    let new_li = document.createElement("div")
    new_li.className = "col-6 mb-3"
    new_li.appendChild(label)
    new_li.appendChild(val)

    card_list.appendChild(new_li)
    
  }
  card_wrapper.appendChild(card_header)

  card_col_1.appendChild(card_image)

  card_row.appendChild(card_col_1)
  card_row.appendChild(card_col_2)

  card_body.appendChild(card_row)
  
  card_wrapper.appendChild(card_body)

  // 
  target_element.appendChild(card_wrapper)
}

function showUserDetails(id){
  let param = id.value.split(" - ")[1]
  let contact_splash_image = document.querySelector("#contact_splash_image")
  console.log("Param ", param)
  $.getJSON(`/u/${param}`).then((user) => {
    let person_query = document.querySelector("#person_query")
    let users_list = document.querySelector("#users_lists")

    console.log("user is ", user)
    person_query.classList.toggle("ht-30d")
    person_query.classList.toggle("ht-50d")
    
    users_list.classList.toggle("ht-50d")
    users_list.classList.toggle("ht-70d")

    // contact_splash_image.setAttribute("src", user.thumbnail_url)
    createUserCard(user, "selected_person")
  })
}
function getCrazy(html_output, id){
  let parser = new DOMParser()
  let html = parser.parseFromString(parser, 'text/html')
}
// function getKB(){
//   console.log("This is KB running")
//   fetch("https://app.atera.com/api/v3/knowledgebases", {
//     'headers':{
//       'Content-Type': 'application/json',
//       "X-API-KEY": "Bearer 7c215afdf2a346df8469ba88dc909771",
//       "Access-Control-Allow-Origin": "*"
//     }
//   }).then((kb) => {
//     console.log("This is KB: ", kb.json())
//   })
// }