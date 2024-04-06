<script>
    import {activeAccountId} from "../../store";

    let accountBalancePromise
    $: accountBalancePromise = getAccountBalance($activeAccountId); 

    async function getAccountBalance(accountId){
        const parameters = new URLSearchParams({account_id: accountId});
        const response = await fetch(`/api/v1/accountBalance?${parameters}`, {method: "GET"})
        const results = await response.json() 
        return results
    };

</script>

<div class="container p-2">
{#await accountBalancePromise}
    <span>Stan Konta:</span>
    {:then accountBalance }
    <span>Stan Konta: <strong>{accountBalance.account_balance}</strong></span>
    {:catch Error}
    <span>Błąd pobierania danych</span>
    {/await}
</div>

<style>

</style>
