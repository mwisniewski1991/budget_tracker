const typeInput = document.querySelector("#type_id");
const categoryInput = document.querySelector("#category");
const subcategoryInput = document.querySelector("#subcategory");



async function getCategories(userParameters){

    const parameters = new URLSearchParams(userParameters)
    const resposne = await fetch(`/categories?${parameters}`, {method:"GET"})
    const json = await resposne.json()
    return json

}

async function createNewCategories(categoriesList){
    categoryInput.innerHTML = '';

    categoriesList.forEach(element => {
        const new_option = document.createElement("option");
        new_option.textContent = element.name_pl;
        new_option.value = element.id;

        categoryInput.appendChild(new_option);
    });
}

async function getSubcategories(userParameters){

    const parameters = new URLSearchParams(userParameters)
    const resposne = await fetch(`/subcategories?${parameters}`, {method:"GET"})
    const json = await resposne.json()
    return json
}

async function createNewSubcategories(subcategoriesList){
    subcategoryInput.innerHTML = '';

    subcategoriesList.forEach(element => {
        const new_option = document.createElement("option");
        new_option.textContent = element.name_pl;
        new_option.value = element.id;
        subcategoryInput.appendChild(new_option);
    });
}

typeInput.addEventListener("change", async (event) => {
    const categoriesList = await getCategories({type_id: event.target.value})
    createNewCategories(categoriesList)

    const firstCategoryID = categoriesList[0].id
    const subcategoriesList = await getSubcategories({category_id: firstCategoryID})
    createNewSubcategories(subcategoriesList)
});

categoryInput.addEventListener("change", async (event) => {
    const subcategoriesList = await getSubcategories({category_id: event.target.value})
    createNewSubcategories(subcategoriesList)
});