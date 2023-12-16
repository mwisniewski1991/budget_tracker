<script>
    export let headerIDtoDelete;

    async function deleteHeader(headerID){
        const parameters = new URLSearchParams({headerid: headerID});
        const resposne = await fetch(`/api/v1/position-delete?${parameters}`, {method:"DELETE"})
        const results =  await resposne.json();
        location.reload()
    };

</script>

<button type="button" class="btn btn-danger" on:click={deleteHeader(headerIDtoDelete)}>DELETE</button>            
