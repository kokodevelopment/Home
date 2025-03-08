<script>
    /** @type {import('./$types').PageData} */
    export let data;

    import { onMount } from "svelte";
    import { browser } from '$app/environment';
    import MarkdownIt from "markdown-it";
    import GuidelinePages from "../../../guidelines/pages";

    const markdownSource = GuidelinePages[data.slug] || "404 Page Not Found";
    if (markdownSource === '404 Page Not Found' && browser) {
        location.href = location.origin + '/error?error=404';
    }

    const md = new MarkdownIt({
        html: true,
        linkify: true,
        breaks: true,
    });

    md.renderer.rules.fence = function (tokens, idx) {
        const token = tokens[idx];

        if (token.info === "warning") {
            return `<div class="guidelines-warning-box">${md.utils.escapeHtml(
                token.content
            )}</div>`;
        }

        // By default markdown-it will use a strange combination of <code> and <pre>; we'd rather it
        // just use <pre>
        return `<pre class="language-${md.utils.escapeHtml(
            token.info
        )}">${md.utils.escapeHtml(token.content)}</pre>`;
    };

    const env = {};
    const tokens = md.parse(markdownSource, env);

    const bodyHTML = md.renderer.render(tokens, md.options, env);
</script>

<svelte:head>
    <title>OrangeMod - Uploading Guidelines</title>
    <meta name="title"                   content="OrangeMod - Uploading Guidelines" />
    <meta property="og:title"            content="OrangeMod - Uploading Guidelines" />
    <meta property="twitter:title"       content="OrangeMod - Uploading Guidelines">
    <meta name="description"             content="OrangeMod's official rules on uploaded projects">
    <meta property="twitter:description" content="OrangeMod's official rules on uploaded projects">
    <meta property="og:url"              content="https://pm.kokodev.cc/guidelines/uploading">
    <meta property="twitter:url"         content="https://pm.kokodev.cc/guidelines/uploading">
</svelte:head>

<div class="container">
    {@html bodyHTML}
</div>

<style>
    .container {
        margin: 0 20%;
        width: 60%;
    }
    
    :global(h1),
    :global(h2) {
        color: rgb(255, 140, 0);
    }
    :global(a) {
        color: rgb(255, 131, 30);
    }

    :global(body.dark-mode) :global(h1),
    :global(body.dark-mode) :global(h2) {
        color: rgb(255, 169, 93);
    }
    :global(body.dark-mode) :global(a) {
        color: rgb(255, 154, 30);
    }
</style>
