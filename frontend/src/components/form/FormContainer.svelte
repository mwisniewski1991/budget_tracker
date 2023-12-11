<script>
    import FormHeader from "./FormHeader.svelte";
    import FormTab from "./FormTab.svelte";
</script>

<div class="container-sm">
    <form action="/add" method="post">

    <FormHeader></FormHeader>
    
    <button type="submit" class="btn btn-primary">Prześlij</button>

    <FormTab></FormTab>


    </form>
</div>