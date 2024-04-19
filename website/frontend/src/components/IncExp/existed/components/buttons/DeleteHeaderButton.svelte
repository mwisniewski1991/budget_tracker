<script>
    export let headerIDtoDelete;

    async function deleteHeader(headerID){
        const resposne = await fetch(`/api/v1/position-delete/${headerID}`, {method:"DELETE"})
        location.reload()
    };


</script>

<button type="button" class="btn btn-danger" on:click={deleteHeader(headerIDtoDelete)}>DELETE</button>            
