<script>
    import AddNewAccount from "./AddNewAccount.svelte";
    import Account from "./Account.svelte";
    export let owner_id;
    export let owner_name_pl;
    export let accounts;
</script>


<div class='container container-border p-2'>
    <div class="row">
        <form action="/api/v1/owners" method="post">
            <div class="row">
                <div class="col">
                    <input type="text" class="form-control" id="owner_id" name="owner_id" readonly value={owner_id}>
                </div>
                <div class="col-10">
                    <input type="text" class="form-control" id="owner_name_pl" name="owner_name_pl" value={owner_name_pl}>
                </div>
                <div class="col">
                    <button type="submit" class="btn btn-warning">Zmień</button>
                </div>
                
            </div>
        </form>
    </div>

    <div class="row container-border">
        <h5>Lista kont</h5>
        <AddNewAccount owner_id={owner_id}/>

        {#each accounts as account }
            <Account owner_id={owner_id} account_id={account.account_id} account_name={account.account_name_pl}/>
        {/each}

    </div>
</div>

<style>
    .container-border{
        border: 1px solid white;
        border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>