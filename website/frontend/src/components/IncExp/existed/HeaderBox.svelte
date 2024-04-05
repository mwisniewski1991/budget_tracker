<script>
    import PositionBox from "./PositionBox.svelte";
    import DeleteHeaderButton from "./components/buttons/DeleteHeaderButton.svelte";
    import PostHeaderButton from "./components/buttons/PostHeaderButton.svelte";
    import InPlaceEditHeader from "./inPlaceEdit/InPlaceEditHeader.svelte";

    export let header_id;
    export let type_name;
    export let header_date;
    export let source;
    export let positions;
    export let total_amount;

    export let account_name;
    export let owner_name;

</script>

<div class="container container-border">

    <div class="row">

        <!-- <div class="col"><strong>{header_id}</strong></div> -->
        <div class="col"><strong></strong></div>

        <div class="col">
            {#if type_name.trim() == "Dochód"}
                <InPlaceEditHeader bind:value={type_name } header_id={header_id} inPlaceType='type_name'/>
                <!-- <span class="income-position"><strong>{type_name.trim()}</strong></span> -->

            {:else if type_name.trim() == "Wydatek"}
                <InPlaceEditHeader bind:value={type_name} header_id={header_id} inPlaceType='type_name'/>
                <!-- <span class="expense-position"><strong>{type_name.trim()}</strong></span> -->
            {:else}
                <InPlaceEditHeader bind:value={type_name} header_id={header_id} inPlaceType='type_name'/>
                <!-- <span ><strong>{type_name}</strong></span> -->
            {/if}
        </div>
        
        <InPlaceEditHeader bind:value={header_date} header_id={header_id} inPlaceType='header_date'/>
        <InPlaceEditHeader bind:value={source} header_id={header_id} inPlaceType='source'/>
        <div class="col"><strong>{total_amount}</strong></div>

        
        <!-- <div class="col"><strong>{header_date}</strong></div> -->
        <!-- <div class="col"><strong>{source}</strong></div> -->
        <!-- <div class="col"><strong>{total_amount}</strong></div> -->
        
        <div class="col">
            <PostHeaderButton headerIDtoEdit={header_id}/>
            <DeleteHeaderButton headerIDtoDelete={header_id} />
        </div>


    </div>

    {#each positions as position }
        <PositionBox {...position}/>    
    {/each}

</div>

<style>
    .container-border{
        border: 1px solid white;
        padding: 5px 0px;
        margin-bottom: 20px;
    }
    /* .income-position{
        color: green;
    }
    .expense-position{
        color: red;
    } */


</style>