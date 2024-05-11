<script>
    export let owner_id;
    let method_route = `/api/v1/owners/${owner_id}/accounts`
</script>

    
<h6 class="pt-2">Dodaj nowego konto</h6>

<div class="container">
    <form action={method_route} method="POST">

        <div class="row">
            <div class="col">
                <label for="account_name">Wpisz nazwę</label>
            </div>
            <div class="col">
                <input type="text" id="account_name" name="account_name">
            </div>
            <div class="col">
                <button type="submit" class="btn btn-primary">Prześlij</button>
            </div>

        </div>

    </form>
</div>