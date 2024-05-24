<script>
    import {activeOnwerId, activeAccountId} from "../../../../store.js";
    export let headerIDtoDelete;

    async function deleteHeader(headerID){
        let method_route = `/api/v1/owners/${$activeOnwerId}/accounts/${$activeAccountId}/incexp/${headerID}`
        const resposne = await fetch(method_route, {method:"DELETE"})
        location.reload()
    };


</script>

<button type="button" class="btn btn-danger" on:click={deleteHeader(headerIDtoDelete)}>DELETE</button>            
