<script>
    import InPlaceEdit from "./inPlaceEdit/InPlaceEditHeader.svelte";
    import InPlaceEditPosition from "./inPlaceEdit/InPlaceEditPosition.svelte";

    export let position_id;
    export let category;
    export let subcategory;
    export let amount;

    export let header_id;
</script>


<div class="row">
    <div class="col">{position_id}</div>
    <InPlaceEditPosition bind:value={category} header_id={header_id} position_id={position_id} inPlaceType='category'/>
    <InPlaceEditPosition bind:value={subcategory} header_id={header_id} position_id={position_id} inPlaceType='subcategory'/>
    <div class="col"></div>
    <InPlaceEditPosition bind:value={amount} header_id={header_id} position_id={position_id} inPlaceType='amount'/>
    <div class="col"></div>

    <!-- <div class="col">{position_id}</div>
    <div class="col">{category}</div>
    <div class="col">{subcategory}</div>
    <div class="col"></div>
    <div class="col">{amount}</div>
    <div class="col"></div> -->
</div>