<script>
import {activeOnwerId, activeAccountId} from "../store";
import IncExpNew from "./new/IncExpNew.svelte";
import IncExpExistedList from "./existed/IncExpExistedList.svelte";
import AccountBalance from "./accountBalance/accountBalance.svelte";

let ownersAccountsPromise = getOwnersAccounts()
let ownerAccountObject;

$: activeOnwerAccountId = createActiveOwnerAccountKey($activeOnwerId, $activeAccountId);
const createActiveOwnerAccountKey = (ownerId, accountId) => `${ownerId}_${accountId}`;

async function getOwnersAccounts(){
    const response = await fetch('/api/v1/owners-accounts')
    const results = await response.json()
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

<div class="container">
        <label for="owner_id" class="form-label">Właściciel</label>
        <select class="form-select" aria-label="Default select example" id="owner_id" name="owner_id" bind:value={ownerAccountObject} on:change={onOwnerAccountChange(ownerAccountObject)}>

            {#await ownersAccountsPromise}
                <option value=""></option>
            {:then ownersAccountsList }
                {#each ownersAccountsList as ownerAccount }

                    {#if createActiveOwnerAccountKey(ownerAccount.owner_id, ownerAccount.account_id) == activeOnwerAccountId}    
                        <option selected value="{ownerAccount.owner_id}_{ownerAccount.account_id}" >{ownerAccount.owner_name_pl} - {ownerAccount.account_name_pl}</option>
                    {:else}
                        <option value="{ownerAccount.owner_id}_{ownerAccount.account_id}" >{ownerAccount.owner_name_pl} - {ownerAccount.account_name_pl}</option>
                    {/if}

                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}

        </select>
</div>    

<AccountBalance/>
<IncExpNew/>
<IncExpExistedList/>