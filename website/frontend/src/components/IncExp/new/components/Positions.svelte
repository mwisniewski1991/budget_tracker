<script>
    import CategoryForm from "./positionFormElements/CategoryForm.svelte";
    import SubcategoryForm from "./positionFormElements/SubcategoryForm.svelte";
    import AmountForm from "./positionFormElements/AmountForm.svelte";
    import CommentForm from "./positionFormElements/CommentForm.svelte";
    import ConnectionForm from "./positionFormElements/ConnectionForm.svelte"
    
    export let positionId;
    export let currentTypeId;
    let currentPostionCategory;

</script>


<div class="container container-border">
    <div class="row">
        <div class="col">{positionId}</div>
        <div class="col-4"><CategoryForm positionId={positionId} currentTypeId={currentTypeId} bind:currentPostionCategory/></div>
        <div class="col-4"><SubcategoryForm positionId={positionId} currentTypeId={currentTypeId} currentPostionCategory={currentPostionCategory}/></div>
        <div class="col"><AmountForm positionId={positionId}/></div>
    </div>

    <div class="row">
        <div class="col"><CommentForm positionId={positionId}/></div>
        <div class="col"><ConnectionForm positionId={positionId}/></div>
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