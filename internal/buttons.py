from aiogram import types

def key_sel_stand():
    st = types.InlineKeyboardMarkup(resize_keyboard=True)
    st.add(types.InlineKeyboardButton(text="✅ dev", callback_data=f"dev",))
    st.add(types.InlineKeyboardButton(text="✅ uat", callback_data=f"uat"))
    st.add(types.InlineKeyboardButton(text="✅ pprod", callback_data=f"pprod"))
    st.add(types.InlineKeyboardButton(text="✅ gitlab_open_issue", callback_data=f"gitlab_open_issue"))
    return st

def key_sel_ns():
    ns = types.InlineKeyboardMarkup(resize_keyboard=True)
    ns.row((types.InlineKeyboardButton(text="default", callback_data=f"default")), (types.InlineKeyboardButton(text="gitlab", callback_data=f"gitlab")),
           (types.InlineKeyboardButton(text="ingress-nginx", callback_data=f"ingress-nginx" )), (types.InlineKeyboardButton(text="kube-system", callback_data=f"kube-system")))
    ns.row((types.InlineKeyboardButton(text="lkl", callback_data=f"lkl" )), (types.InlineKeyboardButton(text="longhorn-system", callback_data=f"longhorn-system")),
           (types.InlineKeyboardButton(text="pam", callback_data=f"pam")), (types.InlineKeyboardButton(text="phd", callback_data=f"phd")))
    ns.row((types.InlineKeyboardButton(text="pia", callback_data=f"pia")), (types.InlineKeyboardButton(text="pib", callback_data=f"pib")),
           (types.InlineKeyboardButton(text="pil", callback_data=f"pil")), (types.InlineKeyboardButton(text="plk", callback_data=f"plk")))
    ns.row((types.InlineKeyboardButton(text="pnsi",callback_data=f"pnsi")), (types.InlineKeyboardButton(text="popd", callback_data=f"popd")),
           (types.InlineKeyboardButton(text="pozvl", callback_data=f"pozvl")), (types.InlineKeyboardButton(text="ppod", callback_data=f"ppod")))
    ns.row((types.InlineKeyboardButton(text="pub", callback_data=f"pub")), (types.InlineKeyboardButton(text="pud", callback_data=f"pud")),
           (types.InlineKeyboardButton(text="pul", callback_data=f"pul")), (types.InlineKeyboardButton(text="pup", callback_data=f"pup")))
    ns.row((types.InlineKeyboardButton(text="pv", callback_data=f"pv")), (types.InlineKeyboardButton(text="pvv", callback_data=f"pvv")))
    return ns

def key_sel_cmd():
    cmd = types.InlineKeyboardMarkup(resize_keyboard=True)
    cmd.row((types.InlineKeyboardButton(text="get pv", callback_data=f"get_pv")), (types.InlineKeyboardButton(text="get ingress", callback_data=f"get_ingress")))
    cmd.row((types.InlineKeyboardButton(text="get pods", callback_data=f"get_pods")), (types.InlineKeyboardButton(text="get deploy", callback_data=f"get_deploy")))
    cmd.row((types.InlineKeyboardButton(text="get ns", callback_data=f"get_ns" )), (types.InlineKeyboardButton(text="get nodes", callback_data=f"get_nodes" )))
    cmd.row((types.InlineKeyboardButton(text="Back 🔁", callback_data=f"Back")), (types.InlineKeyboardButton(text="get event", callback_data=f"get_event")))
    return cmd
