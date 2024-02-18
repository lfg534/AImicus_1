from set_context import set_context

# 用户名
user_name = 'User'
gpt_name = 'AImicus'
# 头像(svg格式) 来自 https://www.dicebear.com/playground?style=identicon
user_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5 5" fill="none" shape-rendering="crispEdges" width="512" height="512"><desc>"Identicon" by "Florian Körner", licensed under "CC0 1.0". / Remix of the original. - Created with dicebear.com</desc><metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:RDF><cc:Work><dc:title>Identicon</dc:title><dc:creator><cc:Agent rdf:about="https://dicebear.com"><dc:title>Florian Körner</dc:title></cc:Agent></dc:creator><dc:source>https://dicebear.com</dc:source><cc:license rdf:resource="https://creativecommons.org/publicdomain/zero/1.0/" /></cc:Work></rdf:RDF></metadata><mask id="viewboxMask"><rect width="5" height="5" rx="0" ry="0" x="0" y="0" fill="#fff" /></mask><g mask="url(#viewboxMask)"><path fill="#c0ca33" d="M2 0h1v1H2z"/><path fill="#c0ca33" d="M1 1h3v1H1z"/><path fill="#c0ca33" d="M0 2h5v1H0z"/><path fill="#c0ca33" d="M1 3h3v1H1z"/><path d="M0 4h1v1H0V4ZM4 4h1v1H4V4ZM3 4H2v1h1V4Z" fill="#c0ca33"/></g></svg>"""
gpt_svg ="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" fill="none" shape-rendering="auto" width="512" height="512"><desc>"Bottts" by "Pablo Stanley", licensed under "Free for personal and commercial use". / Remix of the original. - Created with dicebear.com</desc><metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:RDF><cc:Work><dc:title>Bottts</dc:title><dc:creator><cc:Agent rdf:about="https://twitter.com/pablostanley"><dc:title>Pablo Stanley</dc:title></cc:Agent></dc:creator><dc:source>https://bottts.com/</dc:source><cc:license rdf:resource="https://bottts.com/" /></cc:Work></rdf:RDF></metadata><mask id="viewboxMask"><rect width="180" height="180" rx="0" ry="0" x="0" y="0" fill="#fff" /></mask><g mask="url(#viewboxMask)"><g transform="translate(0 66)"><path d="M38 12c-2.95 11.7-19.9 6.67-23.37 18-3.46 11.35 8.03 20 17.53 20" stroke="#2A3544" stroke-width="6" opacity=".9"/><path d="M150 55c8.4 3.49 20.1-7.6 16-16.5-4.1-8.9-16-6.7-16-19.3" stroke="#2A3544" stroke-width="4" opacity=".9"/><mask id="sidesCables01-a" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="21" y="6" width="138" height="58"><g fill="#fff"><rect x="21" y="35" width="16" height="22" rx="2"/><rect x="136" y="42" width="23" height="22" rx="2"/><rect x="136" y="6" width="23" height="18" rx="2"/></g></mask><g mask="url(#sidesCables01-a)"><path d="M0 0h180v76H0V0Z" fill="#00acc1"/><path d="M0 0h180v76H0V0Z" fill="#fff" fill-opacity=".3"/></g></g><g transform="translate(41)"><g filter="url(#topGlowingBulb02-a)"><path fill-rule="evenodd" clip-rule="evenodd" d="M30 33a20 20 0 1 1 40 0v11H30V33Z" fill="#fff" fill-opacity=".3"/></g><ellipse cx="50" cy="30" rx="4" ry="6" fill="#fff" fill-opacity=".6"/><path d="M50 15.5c4.93 0 9.37 2.13 12.44 5.52m2.43 3.5c.7 1.3 1.21 2.73 1.53 4.23" stroke="#fff" stroke-width="2" stroke-linecap="round"/><rect x="20" y="36" width="60" height="16" rx="1" fill="#48494B"/><defs><filter id="topGlowingBulb02-a" x="22" y="5" width="56" height="47" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feColorMatrix in="SourceAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/><feOffset/><feGaussianBlur stdDeviation="4"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.5 0"/><feBlend in2="BackgroundImageFix" result="effect1_dropShadow_617_633"/><feBlend in="SourceGraphic" in2="effect1_dropShadow_617_633" result="shape"/><feColorMatrix in="SourceAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/><feOffset/><feGaussianBlur stdDeviation="2"/><feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.5 0"/><feBlend in2="shape" result="effect2_innerShadow_617_633"/></filter></defs></g><g transform="translate(25 44)"><mask id="faceSquare02-a" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="0" y="0" width="130" height="120"><path d="M0 12A12 12 0 0 1 12 0h106a12 12 0 0 1 12 12v70a38 38 0 0 1-38 38H38A38 38 0 0 1 0 82V12Z" fill="#fff"/></mask><g mask="url(#faceSquare02-a)"><path d="M-2-2h134v124H-2V-2Z" fill="#00acc1"/><g transform="translate(-1 -1)"></g></g></g><g transform="translate(52 124)"><rect x="24" y="6" width="27" height="8" rx="4" fill="#000" fill-opacity=".8"/></g><g transform="translate(38 76)"><rect y="4" width="104" height="42" rx="4" fill="#000" fill-opacity=".8"/><rect x="28" y="25" width="10" height="11" rx="2" fill="#8BDDFF"/><rect x="66" y="25" width="10" height="11" rx="2" fill="#8BDDFF"/><path fill-rule="evenodd" clip-rule="evenodd" d="M21 4h8L12 46H4L21 4Z" fill="#fff" fill-opacity=".4"/></g></g></svg>"""

# 内容背景
user_background_color = ''
gpt_background_color = 'rgba(225, 230, 235, 0.5)'
# 模型初始设置
initial_content_all = {
    "history": [
        {
            "role": "assistant",
            "content": "您好，我是**AImicus**，我是一款由讯飞星火大模型支持的AI智能**起诉状生成**小助手！\n\n只要您将必要信息提供给我，我就可以按您的要求生成一份合格准确的起诉状！现在，我需要知道您起诉的**案由**，也就是案件的主题。\n\n您可以回答：\n\n  * **民间借贷纠纷** \n\n * **机动车交通事故责任纠纷** \n\n * 或：其他您需处理的事故纠纷类型。"
        }
    ],
    "paras": {
        "temperature": 1.0,
        "top_p": 1.0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
    },
    "contexts": {
        'context_select': '不设置',
        'context_input': '',
        'context_level': 4
    }
}
# 上下文
set_context_all = {"不设置": ""}
set_context_all.update(set_context)

# 自定义css、js
css_code = """
    <style>
    [data-testid="stDecoration"] {
    background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
    }

    section[data-testid="stSidebar"] > div > div:nth-child(2) {
        padding-top: 0.75rem !important;
    }
    
    section.main > div {
        padding-top: 10px;
    }
    
    section[data-testid="stSidebar"] h1 {
        text-shadow: 2px 2px #ccc;
        font-size: 28px !important;
        font-family: "微软雅黑", "auto";
        margin-bottom: 6px;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio {
        overflow: overlay;
        height: 28vh;
    }
    
    hr {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    .avatar {
        display: flex;
        align-items: center;
        gap: 10px;
        pointer-events: none;
        margin: -8px 10px -16px;
    }
    
    .avatar svg {
        width: 15px;
        height: 15px;
    }
    
    .avatar h2 {
        font-size: 16px;
        margin: 0;
    }
    
    .content-div {
        padding: 5px 20px;
        margin: 5px;
        text-align: left;
        border-radius: 10px;
        border: none;
        line-height: 1.6;
        font-size: 12px;
    }
    
    .content-div.assistant p {
        padding: 4px;
        margin: 2px;
    }
    
    .content-div.user p {
        padding: 4px;
        margin: -5px 2px -3px;
    }

   

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    button[kind="primaryFormSubmit"] {
        border: none;
        padding: 0;
    }
    
    div[data-testid="stForm"] + div[data-testid="stHorizontalBlock"] div[data-baseweb="select"] > div:nth-child(1) {
        background-color: transparent;
        justify-content: center;
        font-weight: 300;
        border-radius: 0.25rem;
        margin: 0;
        line-height: 1.2;
        border: 1px solid rgba(49, 51, 63, 0.2);
    }
    </style>
"""

js_code = """
<script>
function checkElements() {
    const textinput = window.parent.document.querySelector("textarea[aria-label='**输入：**']");   //label需要相对应
    const textarea = window.parent.document.querySelector("div[data-baseweb = 'textarea']");
    const button = window.parent.document.querySelector("button[kind='secondaryFormSubmit']");
    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"] p');
    const tabs_div = window.parent.document.querySelector('div[role="tablist"]');
    const tab_panels = window.parent.document.querySelectorAll('div[data-baseweb="tab-panel"]');

    if (textinput && textarea && button && tabs && tabs_div && tab_panels) {
        // 双击点位输入框，同时抑制双击时选中文本事件
        window.parent.document.addEventListener('dblclick', function (event) {
            let activeTab = tabs_div.querySelector('button[aria-selected="true"]');
            if (activeTab.querySelector('p').textContent === '💬 聊天') {
                textinput.focus();
            } else {
                tabs[0].click();
                const waitMs = 50;

                function waitForFocus() {
                    if (window.parent.document.activeElement === textinput) {
                    } else {
                        setTimeout(function () {
                            textinput.focus();
                            waitForFocus();
                        }, waitMs);
                    }
                }

                waitForFocus();
            }
        });
        window.parent.document.addEventListener('mousedown', (event) => {
            if (event.detail === 2) {
                event.preventDefault();
            }
        });
        textinput.addEventListener('focusin', function (event) {
            event.stopPropagation();
            textarea.style.borderColor = 'rgb(0,102,204)';
        });
        textinput.addEventListener('focusout', function (event) {
            event.stopPropagation();
            textarea.style.borderColor = 'white';
        });

        // Ctrl + Enter快捷方式
        window.parent.document.addEventListener("keydown", event => {
            if (event.ctrlKey && event.key === "Enter") {
                if (textinput.textContent !== '') {
                    button.click();
                }
                textinput.blur();
            }
        });

        // 设置 Tab 键
        textinput.addEventListener('keydown', function (event) {
            if (event.keyCode === 9) {
                // 阻止默认行为
                event.preventDefault();
                if (!window.parent.getSelection().toString()) {
                    // 获取当前光标位置
                    const start = this.selectionStart;
                    const end = this.selectionEnd;
                    // 在光标位置插入制表符
                    this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
                    // 将光标移动到插入的制表符之后
                    this.selectionStart = this.selectionEnd = start + 1;
                }
            }
        });

        // 处理tabs 在第一次切换时的渲染问题
        tabs.forEach(function (tab, index) {
            const tab_panel_child = tab_panels[index].querySelectorAll("*");

            function set_visibility(state) {
                tab_panels[index].style.visibility = state;
                tab_panel_child.forEach(function (child) {
                    child.style.visibility = state;
                });
            }

            tab.addEventListener("click", function (event) {
                set_visibility('hidden')

                let element = tab_panels[index].querySelector('div[data-testid="stVerticalBlock"]');
                let main_block = window.parent.document.querySelector('section.main div[data-testid="stVerticalBlock"]');
                const waitMs = 50;

                function waitForLayout() {
                    if (element.offsetWidth === main_block.offsetWidth) {
                        set_visibility("visible");
                    } else {
                        setTimeout(waitForLayout, waitMs);
                    }
                }

                waitForLayout();
            });
        });
    } else {
        setTimeout(checkElements, 100);
    }
}

checkElements()
</script>
"""
