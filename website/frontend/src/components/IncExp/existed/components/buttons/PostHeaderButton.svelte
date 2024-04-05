<script>
    export let isModifyMode;
    export let headerIDtoEdit;
    import { incexpList } from "../../../../store";


    async function editHeader(headerID, val){
        
        console.log($incexpList.filter((header_row) => header_row['header_id'] ===  headerID));

        // const parameters = new URLSearchParams({headerid: headerID});
        // const resposne = await fetch(`/api/v1/position-delete?${parameters}`, {method:"DELETE"})
        // const results =  await resposne.json();
        // location.reload()
    };


</script>

{#if isModifyMode}
    <!-- <button type="button" class="btn btn-warning" on:click={editHeader(headerIDtoEdit, false)}>POST</button>    -->
    <button type="submit" class="btn btn-warning">POST</button>            

{:else}
    <button disabled type="button" class="btn btn-warning" on:click={editHeader(headerIDtoEdit, false)}>POST</button>            
{/if}


