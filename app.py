import gradio as gr
import accountService


# ========== Gradio 界面构建 ==========
with gr.Blocks(title="蛔虫君经典旧世", theme=gr.themes.Default()) as app:
    # 顶部 Banner
    with gr.Row():
        gr.Image(
            "bg-reg.jpg", 
            show_label=False,
            show_download_button=False,
            container=False
        )
    
    # Tab界面
    # 修改Tabs组件，使其居中显示
    with gr.Tabs() as tabs:
        # 注册Tab
        with gr.Tab("👤 账号注册"):
            # 居中主要内容区域
            with gr.Row():
                
                with gr.Column():
                    with gr.Group():
                        gr.Markdown("""<div style="background-color: #e3f2fd; 
                          padding: 12px; border-radius: 8px; border-left: 4px solid #2196f3;">
                          <h4 style="margin: 0; color: #1976d2; font-weight: 600;">账户信息</h4>
                          </div>""")
                        username = gr.Textbox(
                            label="👤 用户名", 
                            placeholder="请输入您的游戏用户名",
                            max_lines=1
                        )
                        password = gr.Textbox(
                            label="🔒 密码", 
                            type="password", 
                            placeholder="至少6位字符",
                            max_lines=1
                        )
                        
                    with gr.Group():
                        gr.Markdown("""<div style="background-color: #e3f2fd; 
                          padding: 12px; border-radius: 8px; border-left: 4px solid #2196f3;">
                          <h4 style="margin: 0; color: #1976d2; font-weight: 600;">联系信息</h4>
                          </div>""")
                        email = gr.Textbox(
                            label="✉️ 邮箱地址", 
                            placeholder="example@domain.com",
                            max_lines=1
                        )

                    with gr.Group():
                        gr.Markdown("""<div style="background-color: #e3f2fd; 
                          padding: 12px; border-radius: 8px; border-left: 4px solid #2196f3;">
                          <h4 style="margin: 0; color: #1976d2; font-weight: 600;">其他设置</h4>
                          </div>""")
                        gm_level = gr.Dropdown(
                            label="🚩 GM权限等级", 
                            choices=[
                                ("普通用户", "0"), 
                                ("初级管理员", "1"), 
                                ("高级管理员", "2"), 
                                ("超级管理员", "3")
                            ], 
                            value="0",
                        )

                    submit_btn = gr.Button(
                        "✅️ 立即注册", 
                        variant="primary",
                        scale=1
                    )
                    
                    output = gr.Textbox(
                        label="注册结果", 
                        interactive=False,
                        show_copy_button=True
                    )
                

        # 角色查询Tab
        with gr.Tab("🔍 角色查询") as character_query_tab:
            with gr.Row():
                with gr.Column():
                    # 查询条件区域
                    with gr.Group():
                        with gr.Row():
                            character_name_filter = gr.Textbox(
                                label="👤 角色名",
                                placeholder="请输入角色名进行模糊查询",
                                max_lines=1
                            )
                            online_status_filter = gr.Dropdown(
                                label="🌐 在线状态",
                                choices=[("全部", "all"), ("在线", "online"), ("离线", "offline")],
                                value="all",
                                interactive=True
                            )
                        with gr.Row():
                            search_btn = gr.Button("🔍 查询", variant="primary")

                    with gr.Group():
                        with gr.Row():
                            character_table = gr.Dataframe(
                                headers=["角色名", "等级", "种族", "职业", "性别", "经验值", "金钱", "在线状态", "总在线时间", "最后下线时间", "当前位置"],
                                datatype=["str", "number", "str", "str", "str", "str", "str", "str", "str", "str", "str"],
                                interactive=False,
                                value=[["角色名", "等级", "种族", "职业", "性别", "经验值", "金钱", "在线状态", "总在线时间", "最后下线时间", "当前位置"]]  # 添加表头作为初始值
                            )

    # 事件处理
    submit_btn.click(
        fn=accountService.register_user,
        inputs=[username, password, gm_level, email],
        outputs=output,
    )
    

    # 查询按钮事件
    search_btn.click(
        fn=accountService.get_all_characters,
        inputs=[character_name_filter, online_status_filter],
        outputs=[character_table]
    )

    # 标签页切换事件 - 当切换到角色查询标签页时自动执行查询
    character_query_tab.select(
        fn=accountService.get_all_characters,
        inputs=[character_name_filter, online_status_filter],
        outputs=[character_table]
    )

# ========== 启动应用 ==========
if __name__ == "__main__":
    print("应用启动，访问地址: http://0.0.0.0:7860")
    app.launch(server_name="0.0.0.0", 
        server_port=7860)