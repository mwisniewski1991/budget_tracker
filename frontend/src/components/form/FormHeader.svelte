<script>
    import { userTypeId, userOwnerId, userAccountId, billTotalAmount } from '../store.js';
    import { onMount } from 'svelte';

    let ownersPromise = getOnwers();
    let accountsPromise;
    
    let userType;
    let userOwner;
    let userAccount;
    let currentAmount;

    let now = new Date(), month, day, year;
    let nowString;

    let typesPromise = getTypes();
    $: accountsPromise = getAccounts($userOwnerId);

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
 
    async function getOnwers(){
        const response = await fetch('/api/v1/owners');
        const owners = await response.json(); 
         
        const fistOwnerId = owners[0].id;
        userOwnerId.set(fistOwnerId);

        return owners;
    };

    async function getAccounts(userOwnerId){
        const parameters = new URLSearchParams({'owner_id': userOwnerId})
        const response = await fetch(`/api/v1/accounts?${parameters}`, {method:"GET"})
        const accounts = await response.json()

        const firstAccountId = accounts[0].id;
        userAccountId.set(firstAccountId);

        return accounts
    };
    
    function onTypeChange(){
        userTypeId.set(userType)
    };

    function onOwnerChange(userOwner){
        userOwnerId.set(userOwner);
    };

    function onAccountChange(userAccount){
        userAccountId.set(userAccount);
    };

</script>


<div class="formHeader">
    <div class="mb-3">
        <label for="date" class="form-label">Data</label>
        <input type="date" class="form-control" id="date" name="date" bind:value={nowString}>
    </div>
        
    <div class="mb-3">
        <label for="owner_id" class="form-label">Właściciel</label>
        <select class="form-select" aria-label="Default select example" id="owner_id" name="owner_id" bind:value={userOwner} on:change={onOwnerChange(userOwner)}>
            {#await ownersPromise}
                <option value=""></option>
            {:then ownersList }
                {#each ownersList as owner }
                    <option value={owner.id}>{owner.name_pl}</option>
                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}
        </select>
    </div>    

        
    <div class="mb-3">
        <label for="account_id" class="form-label">Konto</label>
        <select class="form-select" aria-label="Default select example" id="account_id" name="account_id" bind:value={userAccount} on:change={onAccountChange(userAccount)}>
            
            {#await accountsPromise}
                <option value=""></option>
            {:then accountsList }
                {#each accountsList as account }
                    <option value={account.id}>{account.name_pl}</option>
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

      