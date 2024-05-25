<script>
    import {activeOnwerId, activeAccountId} from "../../store";

    let accountBalancePromise
    $: accountBalancePromise = getAccountBalance($activeOnwerId, $activeAccountId); 

    async function getAccountBalance(ownerId, accountId){
        const response = await fetch(`/api/v1/owners/${ownerId}/accounts/${accountId}/balance`, {method: "GET"})
        const results = await response.json() 
        return results
    };

</script>

<div class="container p-2">
{#await accountBalancePromise}
    <span>Stan Konta: ______</span>
    {:then accountBalance }
    <span>Stan Konta: <strong>{accountBalance.account_balance}</strong></span>
    {:catch Error}
    <span>Błąd pobierania danych</span>
    {/await}
</div>

<style>

</style>
