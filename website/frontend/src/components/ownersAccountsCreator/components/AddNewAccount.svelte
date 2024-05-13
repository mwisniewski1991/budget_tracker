<script>
    export let owner_id;
    let method_route = `/api/v1/owners/${owner_id}/accounts`
</script>

    
<div class="row m-2 p-2 border border-white rounded">

    <!-- <h6 class="pt-2">Dodaj nowego konto</h6> -->

    <form action={method_route} method="POST">

        <div class="row">
            <div class="col">
                <span class="mx-auto align-middle">Dodaj nowe konto:</span>
            </div>
            <div class="col">
                <input type="text" id="account_name" name="account_name" placeholder="Wpisz nazwę">
            </div>
            <div class="col">
                <button type="submit" class="btn btn-primary">Dodaj</button>
            </div>

        </div>

    </form>
</div>
