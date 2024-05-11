<script></script>

    
<h4 class="pt-2">Dodawanie nowego właścicela</h4>

<div class="container">
    <form action='/api/v1/owners' method="POST">

        <div class="row">
            <div class="col">
                <label for="owner_name">Wpisz nazwę</label>
            </div>
            <div class="col">
                <input type="text" id="owner_name" name="owner_name">
            </div>
            <div class="col">
                <button type="submit" class="btn btn-primary">Prześlij</button>
            </div>

        </div>

    </form>
</div>