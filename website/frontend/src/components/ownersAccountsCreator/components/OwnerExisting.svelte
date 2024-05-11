<script>
    export let owner_id;
    export let owner_name_pl
</script>


<div class='container'>
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
</div>