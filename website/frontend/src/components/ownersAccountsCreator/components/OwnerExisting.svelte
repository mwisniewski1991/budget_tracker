<script>
    import AddNewAccount from "./AddNewAccount.svelte";
    import Account from "./Account.svelte";
    export let owner_id;
    export let owner_name_pl;
    export let accounts;
</script>


<div class='container p-2 my-4 border border-white rounded'>
    <div class="container">
        <form action="/api/v1/owners" method="post">
            <div class="row">
                <div class="col-2">
                    <input type="text" class="form-control" id="owner_id" name="owner_id" readonly value={owner_id}>
                </div>
                <div class="col-6">
                    <input type="text" class="form-control" id="owner_name_pl" name="owner_name_pl" value={owner_name_pl}>
                </div>
                <div class="col">
                    <button type="submit" class="btn btn-warning">Zmień</button>
                </div>
                
            </div>
        </form>
    </div>

    <div class="container border border-white rounded">
        
        <h5>Lista kont</h5>
        {#each accounts as account }
        <Account owner_id={owner_id} account_id={account.id} account_name={account.name_pl}/>
        {/each}
        
        <AddNewAccount owner_id={owner_id}/>
    </div>
</div>