<script>
    import { onDestroy } from "svelte";
    import { userTypeId, userCategoryId, userSubcategoryId, billTotalAmount   } from "../store.js"

    export let position_id;

    let userCategory;
    let userSubcategory;
    let oldUserAmount = 0.0;
    let userAmount = 0.0;

    let categoriesPromise;
    let subcategoriesPromise;
    
    let htmlPositionId = `pos_${position_id}`;

    let htmlCategoryName = `category_${position_id}`;
    let htmlSubcategoryName = `subcategory_${position_id}`;
    let htmlAmountName = `amount_${position_id}`;
    let htmlCommentName = `comment_${position_id}`;
    let htmlShopName = `shop_${position_id}`;
    let htmlConnectionName = `connection_${position_id}`;

    $: categoriesPromise = getCategories($userTypeId); 
    $: subcategoriesPromise = getSubcategories($userCategoryId); 
    

    function selectClass(position){
        if(position == 1){
            return "tab-pane fade show active"
        }else{
            return "tab-pane fade"
        }
    };

    async function getCategories(userTypeId){
        const parameters = new URLSearchParams({type_id: userTypeId});
        const resposne = await fetch(`/api/v1/categories?${parameters}`, {method:"GET"})
        const categories = await resposne.json()
        
        const fistCategoryValue = categories[0].id
        userCategoryId.set(fistCategoryValue)

        return categories
    };

    async function getSubcategories(userCategoryId){

        const parameters = new URLSearchParams({category_id: userCategoryId});
        const resposne = await fetch(`/api/v1/subcategories?${parameters}`, {method:"GET"})
        const subcategories = await resposne.json()

        const firstSubcategoryOd = subcategories[0].id;
        userSubcategoryId.set(firstSubcategoryOd);

        return subcategories
    };

    function onCategoryChange(userCategory){
        userCategoryId.set(userCategory);
    };

    function onSubcategoryChange(userSubcategory){
        userSubcategoryId.set(userSubcategory);
    };

    function onAmountChange(userValueToAdd){
        let valueToAdd = userValueToAdd;
        if(valueToAdd == null){
            valueToAdd = 0; 
        };

        let billValue;
        billTotalAmount.subscribe((value) => billValue = value);

        billValue = (parseFloat(billValue) - parseFloat(oldUserAmount)).toFixed(2);
        oldUserAmount = valueToAdd;
        billValue = (parseFloat(billValue) + parseFloat(valueToAdd)).toFixed(2);

        billTotalAmount.set(billValue);

    };

    onDestroy(() =>{
        let billValue;
        billTotalAmount.subscribe((value) => billValue = value);
        billValue = billValue - oldUserAmount;
        billTotalAmount.set(billValue);
    });



</script>

<div class={selectClass(position_id)} id={htmlPositionId} role="tabpanel" aria-labelledby="home-tab">

    <div class="position-1">

        <div class="mb-3">
        <label for={htmlCategoryName} class="form-label">Kategoria</label>
            <select class="form-select" aria-label="Default select example" id={htmlCategoryName} name={htmlCategoryName} bind:value={userCategory} on:change={onCategoryChange(userCategory)}>

                {#await categoriesPromise}
                    <p></p>
                {:then categoriesList} 
                        {#each categoriesList as category }
                        <option value={category.id}>{category.name_pl}</option>
                            
                        {/each}
                    {:catch Error}
                        <p>Something went wrong</p>
                {/await}
            </select>
        </div>
        
        <div class="mb-3">
            <label for={htmlSubcategoryName} class="form-label">Podkategoria</label>
            <select class="form-select" aria-label="Default select example" id={htmlSubcategoryName} name={htmlSubcategoryName} bind:value={userSubcategory} on:change={onSubcategoryChange(userSubcategory)}>

                {#await subcategoriesPromise}
                    <p></p>
                {:then subcategoriesList} 
                        {#each subcategoriesList as subcategory }
                        <option value={subcategory.id}>{subcategory.name_pl}</option>
                        {/each}
                    {:catch Error}
                        <p>Something went wrong</p>
                {/await}

            </select>
        </div>

        <div class="mb-3">
            <label for={htmlAmountName} class="form-label">Kwota</label>
            <input type="number" step="0.01" class="form-control" id={htmlAmountName} name={htmlAmountName} bind:value={userAmount} on:input={onAmountChange(userAmount)} >
        </div>
        
        <div class="mb-3">
            <label for={htmlCommentName} class="form-label">Komentarz</label>
            <input type="text" class="form-control" id={htmlCommentName} name={htmlCommentName}>
        </div>

        <div class="mb-3">
            <label for={htmlShopName} class="form-label">Sklep</label>
            <input type="text" class="form-control" id={htmlShopName} name={htmlShopName}>
        </div>

        <div class="mb-3">
        <label for={htmlConnectionName} class="form-label">Powiązanie</label>
        <input type="text" class="form-control" id={htmlConnectionName} name={htmlConnectionName}>
        </div>

    </div>

</div>


