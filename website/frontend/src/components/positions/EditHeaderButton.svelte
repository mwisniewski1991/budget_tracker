<script>
    export let headerIDtoEdit;

    let isEdit = false;

    async function editHeader(headerID, val){
    console.log(headerID);         
        isEdit = val;
        // const parameters = new URLSearchParams({headerid: headerID});
        // const resposne = await fetch(`/api/v1/position-delete?${parameters}`, {method:"DELETE"})
        // const results =  await resposne.json();
        // location.reload()
    };


</script>

{#if isEdit}
<button type="button" class="btn btn-info" on:click={editHeader(headerIDtoEdit, false)}>ENTER</button>            
{:else}
<button type="button" class="btn btn-info" on:click={editHeader(headerIDtoEdit, true)}>EDIT</button>            
{/if}
