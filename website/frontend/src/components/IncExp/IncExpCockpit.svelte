<script>
import {activeOnwerId, activeAccountId} from "../store";
import IncExpNew from "./new/IncExpNew.svelte";
import IncExpExistedList from "./existed/IncExpExistedList.svelte";
import AccountBalance from "./accountBalance/accountBalance.svelte";

let ownersPromise = getOwners()
let ownerAccountObject;

$: activeOnwerAccountId = createActiveOwnerAccountKey($activeOnwerId, $activeAccountId);
const createActiveOwnerAccountKey = (ownerId, accountId) => `${ownerId}_${accountId}`;

async function getOwners(){
    const response = await fetch('/api/v1/owners')
    const results = await response.json()
    console.log(results)
    return results
};

function onOwnerAccountChange(ownerAccountObject){
        let newOwnerId;
        let newAccountID;
        [newOwnerId, newAccountID] = ownerAccountObject.split('_');

        activeOnwerId.set(newOwnerId);
        activeAccountId.set(newAccountID);

        localStorage.setItem("activeOnwerIdLocalData", newOwnerId);
        localStorage.setItem("activeAccountIdLocalData", newAccountID);
    };

</script>

<h3 class="pt-2">Właściciel</h3>
<div class="container">
        <select class="form-select" aria-label="Default select example" id="owner_id" name="owner_id" bind:value={ownerAccountObject} on:change={onOwnerAccountChange(ownerAccountObject)}>

            {#await ownersPromise}
                <option value=""></option>
            {:then owners }
                {#each owners as owner }
                    {#each owner.accounts as account }

                        {#if createActiveOwnerAccountKey(owner.owner_id, owner.account_id) == activeOnwerAccountId}    
                            <option selected value="{owner.id}_{account.id}" >{owner.name_pl} - {account.name_pl}</option>
                        {:else}
                            <option value="{owner.id}_{account.id}" >{owner.name_pl} - {account.name_pl}</option>
                        {/if}
                        
                    {/each}
                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}

        </select>
</div>    


<AccountBalance/>

<IncExpNew/>


<IncExpExistedList/>