<script>
    import { userTypeId, userOwnerId } from '../store.js';

    let ownersPromise = getOnwers();
    let accountsPromise;
    
    let userType;
    let userOwner;

    $: accountsPromise = getAccounts($userOwnerId);


    function onTypeChange(){
        userTypeId.set(userType)
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
        return accounts
    };

    function onOwnerChange(userOwner){
        userOwnerId.set(userOwner);
    };

</script>


<div class="formHeader">
    <div class="mb-3">
        <label for="date" class="form-label">Data</label>
        <input type="date" class="form-control" id="date" name="date">
    </div>
        
    <div class="mb-3">
        <label for="account_id" class="form-label">Właściciel</label>
        <select class="form-select" aria-label="Default select example" id="account_id" name="account_id" bind:value={userOwner} on:change={onOwnerChange(userOwner)}>
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
        <select class="form-select" aria-label="Default select example" id="account_id" name="account_id">
            
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

            <option value="2">Wydatek</option>
            <option value="1">Dochód</option>

        </select>
    </div>    

</div>

      