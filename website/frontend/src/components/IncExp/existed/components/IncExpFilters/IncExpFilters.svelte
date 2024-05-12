<script>
    import LimitFilter from "./components/LimitFilter.svelte";
    import DetailsFilter from "./components/DetailsFilter.svelte";
    import TypeFilter from "./components/TypeFilter.svelte";
    import CategoryFilter from "./components/CategoryFilter.svelte";
    import SubcategoryFilter from "./components/SubcategoryFilter.svelte";
    import CommentsFilter from "./components/CommentsFilter.svelte";
    import ConnectionFilter from "./components/ConnectionFilter .svelte";

    export let typesCategoriesSubcategories;
    export let componentTypeFilter;
    export let componentCategoryFilter;
    export let componentSubcategoryFilter;
    export let componentCommentFilter;
    export let componentConnectionFilter;

</script>
<div class="container container-border">
    <h3>Filtruj</h3>

    <div class="row">
        <div class="col"><LimitFilter/></div>
        <div class="col"><DetailsFilter/></div>
    </div>
    <div class="row">
        <div class="col"><TypeFilter 
                        typesCategoriesSubcategories={typesCategoriesSubcategories} 
                        bind:componentTypeFilter/></div>
                        
                        <div class="col"><CategoryFilter 
                            typesCategoriesSubcategories={typesCategoriesSubcategories} 
                            componentTypeFilter={componentTypeFilter} 
                        bind:componentCategoryFilter/></div>

    <div class="col"><SubcategoryFilter 
                        typesCategoriesSubcategories={typesCategoriesSubcategories}
                        componentTypeFilter={componentTypeFilter}
                        componentCategoryFilter={componentCategoryFilter}
                        bind:componentSubcategoryFilter/></div>
    </div>
    <div class="row">
        <div class="col"><CommentsFilter bind:componentCommentFilter/></div>
        <div class="col"><ConnectionFilter bind:componentConnectionFilter/></div>
        
        
    </div>

</div>

<style>
    .container-border{
        border: 1px solid white;
        border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>