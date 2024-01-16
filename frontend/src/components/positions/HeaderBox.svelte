<script>
    import PositionBox from "./PositionBox.svelte";
    import DeleteHeaderButton from "./DeleteHeaderButton.svelte";

    export let header_id;
    export let type_name;
    export let header_date;
    export let owner_name;
    export let account_name;
    export let positions;
    export let total_amount;

</script>

<div class="container container-border">

    <div class="row">

        <!-- <div class="col"><strong>{header_id}</strong></div> -->
        <div class="col"><strong></strong></div>

        <div class="col">
            {#if type_name.trim() == "Dochód"}
                <span class="income-position"><strong>{type_name.trim()}</strong></span>
            {:else if type_name.trim() == "Wydatek"}
                <span class="expense-position"><strong>{type_name.trim()}</strong></span>
            {:else}
                <span ><strong>{type_name}</strong></span>
            {/if}
        </div>
        
        <div class="col"><strong>{header_date}</strong></div>
        <div class="col"><strong>{owner_name}</strong></div>
        <div class="col"><strong>{total_amount}</strong></div>
        <div class="col">
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
    .income-position{
        color: green;
    }
    .expense-position{
        color: red;
    }


</style>