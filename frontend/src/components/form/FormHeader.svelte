<script>
    import { userTypeId, billTotalAmount } from '../store.js';
    import { onMount } from 'svelte';
    
    let userType;
    let currentAmount;

    let now = new Date(), month, day, year;
    let nowString;
    let typesPromise = getTypes();
    let ownersAccountsPromise = getOwnersAccounts()

    const unsubscribe = billTotalAmount.subscribe((value)=>{
        currentAmount = value;
    });

    onMount(()=> {
        month = '' + (now.getMonth() + 1),
        day = '' + now.getDate(),
        year = now.getFullYear();

        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;

        nowString = [year, month, day].join('-');
	})

    async function getTypes(){
        const response = await fetch('/api/v1/types');
        const types = await response.json();
        
        const firstTypeId = types[0].id;
        userTypeId.set(firstTypeId);

        return types
    };

    async function getOwnersAccounts(){
        const response = await fetch('/api/v1/owners-accounts')
        const results = await response.json()
        return results
    };

    
    function onTypeChange(){
        userTypeId.set(userType)
    };


</script>


<div class="formHeader">

    <div class="mb-3">
        <label for="date" class="form-label">Data</label>
        <input type="date" class="form-control" id="date" name="date" bind:value={nowString}>
    </div>


    <div class="mb-3">
        <label for="owner_account_ids" class="form-label">Właściciel - konto</label>
        <select class="form-select" aria-label="Default select example" id="owner_account_ids" name="owner_account_ids">
            {#await ownersAccountsPromise}
                <option value=""></option>
            {:then ownersAccountsList }
                {#each ownersAccountsList as ownerAccount }
                    <option value="{ownerAccount.owner_id}_{ownerAccount.account_id}" >{ownerAccount.owner_name_pl} -   {ownerAccount.account_name_pl}</option>
                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}
        </select>
    </div>    
    
    <div class="mb-3">
        <label for="type_id" class="form-label">Rodzaj</label>
        <select class="form-select" aria-label="Default select example" id="type_id" name="type_id" bind:value={userType} on:change={onTypeChange}>
            {#await typesPromise}
                <option value=""></option>
            {:then typesList }
                {#each typesList as type }
                    <option value={type.id}>{type.name_pl}</option>
                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}
        </select>
    </div>    

    <div class="mb-3">
        <span>{currentAmount} PLN</span>
    </div>    

</div>

      