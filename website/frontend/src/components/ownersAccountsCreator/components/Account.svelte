<script>
    export let owner_id;
    export let account_id;
    export let account_name;
    let method_route = `/api/v1/owners/${owner_id}/accounts`

</script>

<div class="container">

    <form action={method_route} method="post">
        <div class="row">
            <div class="col-2">
                <input type="text" class="form-control" id="account_id" name="account_id" readonly value={account_id}>
            </div>
            <div class="col-6">
                <input type="text" class="form-control" id="account_name" name="account_name" value={account_name}>
            </div>
            <div class="col">
                <button type="submit" class="btn btn-warning">Zmień</button>
            </div>
            
        </div>
    </form>

</div>

