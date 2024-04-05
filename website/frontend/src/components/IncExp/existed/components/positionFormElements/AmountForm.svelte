<script>
    import { onDestroy } from "svelte";
    import { IncExpNewTotalBillValue  } from "../../../../store"
    
    export let isModifyMode;
    export let positionId;
    export let amount

    let htmlNamePosition = `amount_${positionId}`;
    let oldUserAmount = 0.0;
    let userAmount = parseFloat(0.0).toFixed(2);


    function onAmountChange(userValueToAdd){
        let valueToAdd = userValueToAdd;
        if(valueToAdd == null){
            valueToAdd = 0; 
        };

        let billValue;
        IncExpNewTotalBillValue.subscribe((value) => billValue = value);

        billValue = (parseFloat(billValue) - parseFloat(oldUserAmount)).toFixed(2);
        oldUserAmount = valueToAdd;
        billValue = (parseFloat(billValue) + parseFloat(valueToAdd)).toFixed(2);

        IncExpNewTotalBillValue.set(billValue);

    };

    onDestroy(() =>{
        let billValue;
        IncExpNewTotalBillValue.subscribe((value) => billValue = value);
        billValue = billValue - oldUserAmount;
        IncExpNewTotalBillValue.set(billValue);
    });

</script>

{#if isModifyMode}
    <input type="number" min="0.00" step="0.01" class="form-control" id={htmlNamePosition} name={htmlNamePosition} value={parseFloat(amount).toFixed(2)} on:input={onAmountChange(userAmount)} >
{:else}
    <span>{parseFloat(amount).toFixed(2)}</span>
{/if}