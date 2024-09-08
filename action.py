import random
import asyncio
import time
async def get_clickable_and_focusable_elements(page):
    # 使用可见性过滤器获取当前可见的可点击元素
    #elements = await page.locator(
    #    "button, [role='button'], a, [onclick], input[type='button'], input[type='submit'], button.dft_hide.popup_hide.__ph_btn.__ph_td",
    #).all()
    elements = await page.locator(
        "button:not([disabled]):visible, [role='button']:not([disabled]):visible, a:not([disabled]):visible, input[type='button']:not([disabled]):visible, input[type='submit']:not([disabled]):visible"
    ).all();
    #await elements.wait_for(timeout=2000)

    clickable_and_focusable_elements = []

    #for element in elements:
    #    is_visible = await element.is_visible()
    #    is_enabled = await element.is_enabled()
    #    # 判断元素是否是链接，并且target属性是否为'_blank'
    #    is_link_with_target_blank = await element.evaluate(
    #        "element => element.tagName === 'A' && element.target === '_blank'"
    #    )

        #if is_visible and is_enabled and not is_link_with_target_blank:
    #    if is_visible and is_enabled:
    #        clickable_and_focusable_elements.append(element)

    #return clickable_and_focusable_elements
    return elements


async def random_click_element(page, selector):
    try:
        # 获取元素
        element = await page.query_selector(selector)
        if element:
            # 获取元素的边界框
            bounding_box = await element.bounding_box()
            if bounding_box:
                # 生成随机点击位置
                start_x = random.uniform(bounding_box['x'], bounding_box['x'] + bounding_box['width'])
                start_y = random.uniform(bounding_box['y'], bounding_box['y'] + bounding_box['height'])

                # 执行点击操作
                await page.mouse.click(start_x, start_y)
                print(f"random_click_element Clicked at ({start_x}, {start_y}) within bounding box: {bounding_box}")
            else:
                print("random_click_element Failed to get bounding box for the element.")
        else:
            print(f"random_click_element Element with selector '{selector}' not found on the page.")

    except Exception as e:
        print(f"random_click_element An error occurred: {e}")

async def random_click(page):
    try:
        # 获取当前窗口的句柄
        original_page = page

        # 获取页面上所有可点击的元素
        clickable_elements = await get_clickable_and_focusable_elements(page)

        if clickable_elements:
            # 随机选择一个可点击的元素
            element = random.choice(clickable_elements)
            # 获取元素的位置信息
            bounding_box = await element.bounding_box()
            if bounding_box:
                # 随机生成点击点
                x = random.uniform(bounding_box['x'], bounding_box['x'] + bounding_box['width'])
                y = random.uniform(bounding_box['y'], bounding_box['y'] + bounding_box['height'])

                # 滚动到随机点击点
                await page.evaluate(f"window.scrollTo({x}, {y})")
                await asyncio.sleep(random.uniform(1, 2))  # 停顿一下，模拟人类滚动

                # 点击随机点
                await page.mouse.click(x, y)
                print(f"Clicked on random point ({x}, {y}) within bounding box: {bounding_box}")

                # 检查是否打开了新的标签页
                await page.wait_for_timeout(2000)  # 等待2秒，以确保新标签页打开

                # 获取当前所有标签页
                pages = page.context.pages
                print('xufuhai newpage tab num:', pages, len(pages))
                if len(pages) > 1:
                    print('xufuhai enter new pages')
                    # 获取最后打开的标签页，并切换回原始标签页
                    new_tab = pages[-1]
                    print(f"xufuhai check {new_tab} : {original_page}")
                    if new_tab != original_page:
                        print("Switching back to the original tab.")
                        await original_page.bring_to_front()
                        # 关闭新标签页
                        await new_tab.close()
            else:
                print("Failed to get bounding box for the element.")
        else:
            print("No clickable elements found on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def random_pause():
    # 随机暂停1到10秒
    pause_time = random.uniform(2, 5)
    print(f"Pausing for {pause_time:.2f} seconds")
    await asyncio.sleep(pause_time)

async def wait_for_element_whether_exists(page, element):
    submit_button = await page.query_selector(element)
    print(submit_button, element)
    if submit_button and await submit_button.is_visible():
        time.sleep(5)
        await random_click_element(page, element)
        time.sleep(5)


async def random_scroll_page(page):
    try:
        # 获取页面的总高度
        body_handle = await page.query_selector('body')
        body_box = await body_handle.bounding_box()
        total_height = body_box['height']

        # 随机生成滑动的起点和终点
        start_y = random.uniform(0, total_height - 100)  # 保证滑动不会超出页面
        end_y = random.uniform(start_y, total_height)
        start_x = random.uniform(0, body_box['width'])  # 随机水平位置
        end_x = start_x  # 垂直滑动，不改变水平位置

        # 执行滚动操作
        await page.evaluate(f"window.scrollTo({start_x}, {start_y})")
        await asyncio.sleep(random.uniform(1, 2))  # 模拟人类滚动
        await page.evaluate(f"window.scrollTo({start_x}, {end_y})")

        print(f"Scrolled from ({start_x}, {start_y}) to ({end_x}, {end_y}) on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def random_touch_scroll_page(page):
    try:
        # 获取页面的总高度
        body_handle = await page.query_selector('body')
        body_box = await body_handle.bounding_box()
        total_height = body_box['height']

        # 随机生成滑动的起点和终点
        start_y = random.uniform(0, total_height - 100)  # 保证滑动不会超出页面
        end_y = random.uniform(start_y, total_height)
        start_x = random.uniform(0, body_box['width'])  # 随机水平位置
        end_x = start_x  # 垂直滑动，不改变水平位置

        # 执行触控滑动操作
        await page.touchscreen.tap(start_x, start_y)
        await asyncio.sleep(random.uniform(0.5, 1))
        await page.touchscreen.swipe(start_x, start_y, end_x, end_y)

        print(f"Scrolled from ({start_x}, {start_y}) to ({end_x}, {end_y}) on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def scroll_page(page, is_mobile: bool):
    if is_mobile:
        await random_scroll_page(page)
    else:
        await random_scroll_page(page)