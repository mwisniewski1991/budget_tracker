<script>
    import { incExpFilterDetailsVisible } from "../../../store";

    import CategoryForm from "./positionFormElements/CategoryForm.svelte";
    import SubcategoryForm from "./positionFormElements/SubcategoryForm.svelte";
    import AmountForm from "./positionFormElements/AmountForm.svelte";
    import CommentForm from "./positionFormElements/CommentForm.svelte";
    import ConnectionForm from "./positionFormElements/ConnectionForm.svelte"
    import PositionIdForm from "./positionFormElements/PositionIdForm.svelte";
    
    export let isModifyMode;
    export let currentTypeId;
    export let PositionData;
    export let typeId;
    
    let currentPostionCategory;

</script>

<div class="container container-border">
    <div class="row">
        <div class="col">
            {PositionData['position_id']}
            <PositionIdForm positionId={PositionData['position_id']}/>
        </div>

        <div class="col-4"><CategoryForm 
                                isModifyMode={isModifyMode} 
                                bind:currentPostionCategory
                                typeId={typeId}
                                PositionData={PositionData}
                                currentTypeId={currentTypeId} 
                                /></div>
        
        <div class="col-4"><SubcategoryForm 
                                isModifyMode={isModifyMode} 
                                typeId={typeId}
                                PositionData={PositionData}
                                currentPostionCategory={currentPostionCategory}
                                /></div>
        
        <div class="col"><AmountForm 
                            isModifyMode={isModifyMode} 
                            positionId={PositionData['position_id']} 
                            amount={PositionData['amount']}/></div>

    </div>

    {#if $incExpFilterDetailsVisible === true}
        <div class="row">
            <div class="col"><CommentForm   
                                isModifyMode={isModifyMode} 
                                positionId={PositionData['position_id']} 
                                comment={PositionData['comment']}/></div>

            <div class="col"><ConnectionForm 
                                isModifyMode={isModifyMode} 
                                positionId={PositionData['position_id']} 
                                connection={PositionData['connection']}/></div>
        </div>
    {/if}


</div>


<style>
    .container-border{
        border: 1px solid white;
        border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }

</style>