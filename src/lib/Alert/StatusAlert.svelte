<script>
    import { onMount } from "svelte";
    import Alert from "./Alert.svelte";
    import LINK from "../../resources/urls.js";

    let currentStatus = {
        loading: true,
        updates: [],
    };

    onMount(() => {
        fetch(`${LINK.basicApi}status`).then((res) => {
            if (!res.ok) return;
            res.json().then((status) => {
                // Handle both single and multiple updates
                if (Array.isArray(status)) {
                    currentStatus = {
                        loading: false,
                        updates: status,
                    };
                } else {
                    currentStatus = {
                        loading: false,
                        updates: [status],
                    };
                }
            });
        });
    });

    const defaultButtonText = "Details";
    const defaultButtonHref = "https://status.penguinmod.com/";
    const defaultHasButton = true;
</script>

{#if currentStatus.updates.length > 0}
    {#each currentStatus.updates as update}
        <Alert
            text={update.text}
            backColor={update.type === "warn" ? "#ffd900" : update.type === "error" ? "#ff0000" : "#00ff00"}
            textColor={update.type === "error" ? "white" : "black"}
            hasButton={update.hasButton !== undefined ? update.hasButton : defaultHasButton}
            buttonText={update.buttonText || defaultButtonText}
            buttonHref={update.buttonHref || defaultButtonHref}
            buttonTooLight={update.type === "error" ? false : true}
        />
    {/each}
{/if}
