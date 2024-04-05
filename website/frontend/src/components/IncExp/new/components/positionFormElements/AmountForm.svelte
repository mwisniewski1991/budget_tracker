<script>
    import { onDestroy } from "svelte";
    import { IncExpNewTotalBillValue  } from "../../../../store"
    
    export let positionId;

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


<input type="number" min="0.00" step="0.01" class="form-control" id={htmlNamePosition} name={htmlNamePosition} bind:value={userAmount} on:input={onAmountChange(userAmount)} >